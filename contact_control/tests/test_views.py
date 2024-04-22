from django.test import TestCase  # type: ignore
from django.urls import reverse  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.test import APIClient, APIRequestFactory  # type: ignore
from contact_control.views import ContactViewSet  # type: ignore


class TestRegisterView(TestCase):
    def setUp(self):
        """
        Hook method for setting up the test fixture before exercising it.
        """
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_create_contact_POST(self):
        """
        simple mockup test to simulate creation of contacts
        """
