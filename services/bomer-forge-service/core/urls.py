"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.http import JsonResponse
from django.urls import path, include
from core.google_auth import login_with_google
from django.views.decorators.csrf import ensure_csrf_cookie
from django.middleware.csrf import get_token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.views import SpectacularAPIView


@ensure_csrf_cookie
def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({"csrfToken": csrf_token})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_logged_user(request):
    return JsonResponse({"user": request.user.username, "email": request.user.email})


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/schema.json/", SpectacularAPIView.as_view(), name="schema"),
    path("api/v1/auth/csrf/", get_csrf_token),
    path("api/v1/auth/google/", login_with_google),
    path("api/v1/auth/user/", get_logged_user),
    path("api/v1/", include("projects.rest.urls")),
    path("api/v1/", include("draft_building_designs.rest.urls")),
    path("api/v1/", include("building_components.rest.urls")),
    path("api/v1/", include("celery_worker.rest.urls")),
]
