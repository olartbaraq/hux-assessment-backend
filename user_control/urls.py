from .views import SignUpView, LoginView, LogoutView
from django.urls import path  # type: ignore


urlpatterns = [
    path("api/v1/auth/register/", SignUpView.as_view(), name="register"),
    path("api/v1/auth/login/", LoginView.as_view(), name="login"),
    path("api/v1/auth/logout/", LogoutView.as_view(), name="logout"),
]
