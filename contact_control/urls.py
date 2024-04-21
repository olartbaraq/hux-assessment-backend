from django.urls import path, include  # type: ignore
from rest_framework.routers import DefaultRouter  # type: ignore
from .views import ContactViewSet


router = DefaultRouter(trailing_slash=False)

router.register("create-contact", ContactViewSet, "create a new contact")
router.register("list-contacts", ContactViewSet, "list all contacts")
router.register("get-contact", ContactViewSet, "retrieve a contact")
router.register("update-contact", ContactViewSet, "edit a contact")
router.register("delete-contact", ContactViewSet, "delete a contact")


urlpatterns = [path("", include(router.urls))]
