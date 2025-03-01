from google.oauth2 import id_token
from google.auth.transport import requests
from google.auth.exceptions import MalformedError
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.decorators import api_view
from core.db_constants import constants
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import get_user_model, login

USER_MODEL = get_user_model()


def get_user_for_google_token(token: str) -> User:
    try:
        google_client_id = constants.values().GOOGLE_CLIENT_ID
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), google_client_id
        )
    except MalformedError as e:
        error_message = "Invalid Token: Could not log into Google"
        raise ValueError(error_message) from e

    try:
        return USER_MODEL.objects.get(email=id_info["email"])
    except ObjectDoesNotExist as error:
        error_message = "Google user does not have an account for Backend service for Data Retrieval Platform."
        raise ObjectDoesNotExist(error_message) from error


@api_view(["POST"])
def login_with_google(request):
    try:
        user = get_user_for_google_token(request.data.get("client_token"))
        login(request, user)
        return Response(
            {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
            status=200,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=401)
