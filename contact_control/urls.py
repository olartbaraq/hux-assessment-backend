from django.urls import path, include  # type: ignore
from rest_framework.routers import DefaultRouter  # type: ignore
from .views import ContactViewSet


router = DefaultRouter(trailing_slash=False)

router.register("contact", ContactViewSet, basename="contact")


urlpatterns = [path("", include(router.urls), name="crud-contact")]
