from django.urls import path
from .views import GoogleOauth2LoginApiView

urlpatterns = [
    path("google/login",GoogleOauth2LoginApiView.as_view(), name="google-oauth2-login"),
]
