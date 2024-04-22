from rest_framework.test import APITestCase  # type: ignore
from django.urls import reverse  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.test import APIClient, APIRequestFactory  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from user_control.views import LoginView, SignUpView  # type: ignore


User = get_user_model()


class TestRegisterView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.User = User

    def test_register_user_POST(self):
        # Test data
        user_data = {
            "name": "Mubaraqq",
            "email": "mubby@test2.com",
            "password": "12345678",
        }
        user_data2 = {
            "name": "Mubaraq2",
            "email": "mubby@test3.com",
            "password": "12345678",
        }

        # Create a request using the factory
        request = self.factory.post(reverse("register"), user_data, format="json")

        # Pass the request to the view
        response = SignUpView.as_view()(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(self.User.objects.filter(email="mubby@test2.com").exists())

        # Test with client
        client_response = self.client.post(
            reverse("register"), user_data2, format="json"
        )
        self.assertEqual(client_response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(self.User.objects.filter(email="mubby@test3.com").exists())


class TestLoginView(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()
        self.user = User.objects.create_user(
            email="mubby@test.com",
            password="12345678",
            name="Olart",
        )

    def test_login_user_POST(self):
        user_data = {
            "email": "mubby@test.com",
            "password": "12345678",
        }

        # Create a request using the factory
        request = self.factory.post(reverse("login"), user_data, format="json")

        # Pass the request to the view
        response = LoginView.as_view()(request)

        # Assertions
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data["isLoggedIn"])
        self.assertDictEqual(
            response.data["user"],
            {"email": "mubby@test.com", "name": "Olart", "id": "1"},
        )

        # Test with client
        client_response = self.client.post(reverse("login"), user_data, format="json")
        self.assertEqual(client_response.status_code, status.HTTP_200_OK)

    def tearDown(self):
        self.user.delete()
