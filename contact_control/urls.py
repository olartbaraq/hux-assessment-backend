from .views import CreateContactView, ListContactView, UpdateContactView, RetrieveContactView, DeleteContactView  # type: ignore
from django.urls import path  # type: ignore


urlpatterns = [
    path("contact/create-contact/", CreateContactView.as_view(), name="create-contact"),
    path("contact/list-contacts/", ListContactView.as_view(), name="list-contacts"),
    path(
        "contact/update-contact/<int:pk>/",
        UpdateContactView.as_view(),
        name="update-contact",
    ),
    path(
        "contact/retrieve-contact/<int:pk>/",
        RetrieveContactView.as_view(),
        name="retrieve-contact",
    ),
    path(
        "contact/delete-contact/<int:pk>/",
        DeleteContactView.as_view(),
        name="delete-contact",
    ),
]
