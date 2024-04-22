from .views import SignUpView, LoginView, LogoutView
from django.urls import path  # type: ignore


urlpatterns = [
    path("auth/register/", SignUpView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/logout/", LogoutView.as_view(), name="logout"),
]
