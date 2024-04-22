from rest_framework.test import APITestCase, APIClient  # type: ignore
from django.urls import reverse  # type: ignore
from rest_framework import status  # type: ignore
from contact_control.models import Contact
from django.contrib.auth import get_user_model  # type: ignore


User = get_user_model()


class TestCreateView(APITestCase):
    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="mubby@test.com",
            password="12345678",
            name="Olart",
        )
        self.client.force_authenticate(user=self.user)
        self.contact_data = {
            "lastname": "test1",
            "firstname": "test2",
            "phone_number": "09081235647",
            "user": self.user.id,
        }

    def test_create_contact_POST(self):
        """
        simple mockup test to simulate creation of contacts
        """

        contact_data2 = {
            "lastname": "test1",
            "firstname": "test2",
            "phone_number": "09081235688",
            "user": self.user.id,
        }

        # Create a request using the factory
        response = self.client.post(
            reverse("create-contact"),
            self.contact_data,
            format="json",
        )

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(
            Contact.objects.filter(
                phone_number=self.contact_data["phone_number"]
            ).exists()
        )

        # Test with client
        client_response = self.client.post(
            reverse("create-contact"), contact_data2, format="json"
        )
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(
            Contact.objects.filter(phone_number=contact_data2["phone_number"]).exists()
        )

    def test_list_contacts_GET(self):
        """
        simple mockup test to simulate getting all contacts
        """
        Contact.objects.create(
            lastname="test1",
            firstname="test2",
            phone_number="09081235647",
            user=self.user,
        )
        response = self.client.get(reverse("list-contacts"), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_retrieve_contact_GET(self):
        contact = Contact.objects.create(
            lastname="test1",
            firstname="test2",
            phone_number="09081235647",
            user=self.user,
        )
        response = self.client.get(
            reverse("retrieve-contact", kwargs={"pk": contact.id}), format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["lastname"], "test1")
        self.assertEqual(response.data["firstname"], "test2")
        self.assertNotEqual(response.data["phone_number"], "12345432123")

    def test_update_contact_PUT(self):
        contact = Contact.objects.create(
            lastname="test1",
            firstname="test2",
            phone_number="09081235647",
            user=self.user,
        )
        data = {
            "lastname": "John",
            "firstname": "Smith",
            "phone_number": "1234567890",
            "user": self.user.id,
        }
        response = self.client.put(
            reverse("update-contact", kwargs={"pk": contact.id}),
            data=data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_contact = Contact.objects.get(pk=contact.id)
        self.assertEqual(updated_contact.lastname, "John")
        self.assertEqual(updated_contact.firstname, "Smith")
        self.assertEqual(updated_contact.phone_number, "1234567890")

    # def test_delete_contact_DELETE(self):
    #     contact = Contact.objects.create(
    #         lastname="test1", firstname="test2", phone_number="09081235647"
    #     )
    #     response = self.client.delete(
    #         reverse("contact-detail", kwargs={"pk": contact.id})
    #     )
    #     self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    #     self.assertEqual(Contact.objects.count(), 0)
