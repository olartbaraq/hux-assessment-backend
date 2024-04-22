from rest_framework.test import APITestCase, force_authenticate, APIClient, APIRequestFactory  # type: ignore
from django.urls import reverse  # type: ignore
from rest_framework import status  # type: ignore
from contact_control.views import ContactViewSet  # type: ignore
from contact_control.models import Contact
from django.contrib.auth import get_user_model  # type: ignore
from user_control.tokenauth import JWTAuthentication


User = get_user_model()


class TestCreateView(APITestCase):
    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="mubby@test.com",
            password="12345678",
            name="Olart",
        )
        payload = {"id": self.user.id, "email": self.user.email, "name": self.user.name}

        self.access_token = JWTAuthentication.generate_token(payload=payload)

        # Create a dummy request object
        dummy_request = self.factory.get("api/v1/contact")
        self.auth_user = JWTAuthentication.authenticate(self, dummy_request)

        # Set the authenticated user on the request
        self.request = self.factory.get("api/v1/contact")
        force_authenticate(self.request, user=self.auth_user[0])

        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + str(self.access_token))

    def test_create_contact_POST(self):
        """
        simple mockup test to simulate creation of contacts
        """
        contact_data = {
            "lastname": "test1",
            "firstname": "test2",
            "phone_number": "09081235647",
        }
        contact_data2 = {
            "lastname": "test1",
            "firstname": "test2",
            "phone_number": "09081235688",
        }

        # Create a request using the factory
        request = self.factory.post(
            reverse("contact-list"),
            contact_data,
            format="json",
        )

        # Pass the request to the view
        response = ContactViewSet.as_view({"post": "create"})(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(
            Contact.objects.filter(phone_number=contact_data["phone_number"]).exists()
        )

        # Test with client
        client_response = self.client.post(
            reverse("contact-list"), contact_data2, format="json"
        )
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(
            Contact.objects.filter(phone_number=contact_data["phone_number"]).exists()
        )
