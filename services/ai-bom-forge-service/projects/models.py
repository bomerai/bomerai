from django.db import models
from core.base_model import TimestampedBaseModel
from django.contrib.auth.models import User


class Project(TimestampedBaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    customer_name = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
