"""S3 specific configuration values."""

from core.types.environment import env

__all__ = (
    "S3_ACCESS_KEY",
    "S3_SECRET_ACCESS_KEY",
    "S3_SESSION_PROFILE",
    "S3_ENDPOINT_URL",
    "S3_BUCKET_NAME",
    "S3_USE_SSL",
)

S3_ACCESS_KEY = env.str("S3_ACCESS_KEY", "")
S3_SECRET_ACCESS_KEY = env.str("S3_SECRET_ACCESS_KEY", "")
S3_SESSION_PROFILE = env.str("S3_SESSION_PROFILE", "")
S3_ENDPOINT_URL = env.str("S3_ENDPOINT_URL", "")
S3_BUCKET_NAME = env.str("S3_BUCKET_NAME", "")
S3_USE_SSL = env.bool("S3_USE_SSL", True)
