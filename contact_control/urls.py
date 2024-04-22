from .views import CreateContactView, ListContactView  # type: ignore
from django.urls import path  # type: ignore


urlpatterns = [
    path("contact/create-contact/", CreateContactView.as_view(), name="create-contact"),
    path("contact/list-contacts/", ListContactView.as_view(), name="list-contacts"),
]
