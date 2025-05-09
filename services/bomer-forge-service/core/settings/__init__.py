"""Django settings for protocol_research_service project.

Generated by 'django-admin startproject' using Django 4.2.1 and decomposed
manually.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

# import django_stubs_ext

# import opentelemetry.instrumentation.django
# from django.conf import settings

from .celery import *
from .core import *
from .cors import *
from .logging import *

# django_stubs_ext.monkeypatch()

# opentelemetry.instrumentation.django.DjangoInstrumentor().instrument()

# The opentelemetry call above inserts its middleware at the front of the list,
# but we want to guarantee that our healthcheck middleware is first, because the otel
# middleware indirectly checks the host header, which we do not want to do for healthcheck requests.
# settings.MIDDLEWARE.insert(
#     0, "core.middleware.health_check_middleware.HealthCheckMiddleware"
# )
