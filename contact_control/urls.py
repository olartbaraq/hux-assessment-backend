from .views import CreateContactView  # type: ignore
from django.urls import path  # type: ignore


urlpatterns = [
    path("contact/create-contact/", CreateContactView.as_view(), name="create-contact"),
    # path("auth/login/", LoginView.as_view(), name="login"),
    # path("auth/logout/", LogoutView.as_view(), name="logout"),
]
