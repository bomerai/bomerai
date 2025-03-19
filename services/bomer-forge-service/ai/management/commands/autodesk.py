import base64
import os
import requests
import structlog
from django.core.management.base import BaseCommand

logger = structlog.get_logger(__name__)

AUTODESK_CLIENT_ID = "q81oRFXvTamVGDywhqTRfpuraLIYAFJkBIozJhoLcTltKamg"
AUTODESK_CLIENT_SECRET = (
    "4vdTJGKAZxZAA08k0FbM3gBNYJX2eAfIlRMxM9s53pS3RClLV2fgHnRJNU0YQGis"
)


def get_access_token():
    AUTH_URL = "https://developer.api.autodesk.com/authentication/v2/token"
    payload = {
        "grant_type": "client_credentials",
        "client_id": AUTODESK_CLIENT_ID,
        "client_secret": AUTODESK_CLIENT_SECRET,
        "scope": "data:read data:write data:create bucket:create bucket:read",
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    logger.info("Getting access token", payload=payload)

    response = requests.post(AUTH_URL, data=payload, headers=headers)
    logger.info("Authorized", response=response.json())
    data = response.json()
    return data.get("access_token")


BUCKET_NAME = "beaver-blueprints-bucket"


def create_bucket():
    headers = {
        "Authorization": f"Bearer {os.getenv('AUTODESK_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
    }

    response = requests.post(
        "https://developer.api.autodesk.com/oss/v2/buckets",
        headers=headers,
        json={
            "bucketKey": BUCKET_NAME,
            "policyKey": "transient",
        },  # "transient" = stored for 24 hours
    )

    logger.info("Bucket created", response=response.json())


def upload_file_to_bucket(*, file_path: str):

    headers = {
        "Authorization": f"Bearer {os.getenv('AUTODESK_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
    }

    resp = requests.get(
        f"https://developer.api.autodesk.com/oss/v2/buckets/{BUCKET_NAME}/objects/{file_path.split('/')[-1]}/signeds3upload",
        headers=headers,
    )
    response_data = resp.json()
    if resp.status_code != 200:
        logger.error("Failed to get signed upload details", response=response_data)
        return

    upload_key = response_data["uploadKey"]
    urls = response_data["urls"]
    logger.info(
        "Got signed upload details", upload_key=upload_key, urls_count=len(urls)
    )

    # Read the file data
    with open(file_path, "rb") as f:
        file_data = f.read()

        # Upload each part
        etags = []
        for i, url in enumerate(urls):
            # Calculate the chunk size and data for this part
            chunk_size = 5 * 1024 * 1024  # 5MB chunks
            start = i * chunk_size
            end = min(start + chunk_size, len(file_data))
            chunk = file_data[start:end]

            if not chunk:  # No more data to upload
                break

            # Upload the chunk
            resp = requests.put(url, data=chunk)
            if resp.status_code != 200:
                logger.error(
                    "Part upload failed",
                    part_number=i + 1,
                    status_code=resp.status_code,
                    response=resp.text,
                )
                return
            etags.append(resp.headers.get("ETag"))
            logger.info(f"Uploaded part {i+1}", etag=resp.headers.get("ETag"))

    # Complete the multipart upload
    resp = requests.post(
        f"https://developer.api.autodesk.com/oss/v2/buckets/{BUCKET_NAME}/objects/{file_path.split('/')[-1]}/signeds3upload",
        headers=headers,
        json={
            "uploadKey": upload_key,
            "parts": [
                {"partNumber": i + 1, "eTag": etag.strip('"')}
                for i, etag in enumerate(etags)
            ],
        },
    )

    if resp.status_code != 200:
        logger.error("Failed to complete upload", response=resp.text)
        return

    logger.info("Upload completed successfully", response=resp.json())


def get_object_id_from_file_on_bucket(*, file_name: str) -> str:
    headers = {
        "Authorization": f"Bearer {os.getenv('AUTODESK_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
    }

    resp = requests.get(
        f"https://developer.api.autodesk.com/oss/v2/buckets/{BUCKET_NAME}/objects/{file_name}/details",
        headers=headers,
    )
    if resp.status_code != 200:
        logger.error("Failed to get object ID", response=resp.text)
        return

    logger.info("File downloaded", response=resp.json())
    return resp.json()["objectId"]


def convert_file_for_extraction(urn: str):
    headers = {
        "Authorization": f"Bearer {os.getenv('AUTODESK_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
    }

    # Base64 encode the URN
    encoded_urn = base64.b64encode(urn.encode("utf-8")).decode("utf-8")

    payload = {
        "input": {"urn": encoded_urn},
        "output": {
            "formats": [{"type": "svf", "views": ["2d", "3d"]}, {"type": "obj"}]
        },
    }

    resp = requests.post(
        "https://developer.api.autodesk.com/modelderivative/v2/designdata/job",
        headers=headers,
        json=payload,
    )

    logger.info("Conversion job created", response=resp.json())


def extract_dimensions_from_file(urn: str):
    import json

    headers = {
        "Authorization": f"Bearer {os.getenv('AUTODESK_ACCESS_TOKEN')}",
        "Content-Type": "application/json",
    }

    encoded_urn = base64.b64encode(urn.encode("utf-8")).decode("utf-8")

    resp = requests.get(
        f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{encoded_urn}/metadata",
        headers=headers,
    )

    if resp.status_code != 200:
        logger.error("Failed to extract metadata", response=resp.text)
        return

    logger.info("Metadata extracted", response=resp.json())

    # {
    #     "data": {
    #         "type": "metadata",
    #         "metadata": [
    #             {
    #                 "name": "2D View",
    #                 "role": "2d",
    #                 "guid": "3db1f442-12cc-41e4-c0e5-3fd4fc907287",
    #             },
    #             {
    #                 "name": "3D View",
    #                 "role": "3d",
    #                 "guid": "e30bd031-d13a-a976-9153-78100829986a",
    #             },
    #         ],
    #     }
    # }

    for metadata in resp.json()["data"]["metadata"]:
        resp = requests.get(
            f"https://developer.api.autodesk.com/modelderivative/v2/designdata/{encoded_urn}/metadata/{metadata['guid']}/properties",
            headers=headers,
        )

        logger.info("Properties extracted", response=resp)

        data = resp.json()
        logger.info("Properties data", data=data)
        with open("properties.json", "w") as f:
            json.dump(data, f)

        # rooms = [
        #     item
        #     for item in data["data"]["collection"]
        #     if item["name"].lower().startswith("room")
        # ]

        # for room in rooms:
        #     logger.info(f"Room: {room['name']}, Area: {room['properties']['Area']} m²")


# if __name__ == "__main__":
#     # get_access_token()
#     # create_bucket()
#     # upload_file_to_bucket()
#     object_id = get_object_id_from_file_on_bucket()
#     logger.info("Object ID", object_id=object_id)
#     # convert_file_for_extraction(object_id)
#     # extract_dimensions_from_file(object_id)


class Command(BaseCommand):
    def handle(self, *args, **options):
        token = get_access_token()
        os.environ["AUTODESK_ACCESS_TOKEN"] = token

        file_path = os.path.join(os.path.dirname(__file__), "structure-drawing.dwg")
        upload_file_to_bucket(file_path=file_path)

        object_id = get_object_id_from_file_on_bucket(file_name="structure-drawing.dwg")
        logger.info("Object ID", object_id=object_id)
        convert_file_for_extraction(urn=object_id)
