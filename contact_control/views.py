from django.db import IntegrityError  # type: ignore
from rest_framework.generics import CreateAPIView, ListAPIView  # type: ignore
from .serializers import Contact, ContactSerializer
from rest_framework.permissions import IsAuthenticated  # type: ignore
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.request import Request  # type: ignore
from rest_framework import generics, status  # type: ignore


class CreateContactView(CreateAPIView):
    """this helps create a contact by extending the CreateAPIView post method"""

    serializer_class = ContactSerializer
    permission_classes: list[str] = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Create a Contact")
    def post(self, request: Request):
        """post method to create a contact

        Args:
            request (Request): _description_
        """

        data = request.data
        user = request.user
        valid_request = self.serializer_class(data=data)
        if valid_request.is_valid(raise_exception=True):

            try:

                contact_obj = Contact.objects.create(
                    firstname=valid_request.validated_data["firstname"],
                    lastname=valid_request.validated_data["lastname"],
                    phone_number=valid_request.validated_data["phone_number"],
                    user=user,
                )

                contact_obj.save()
                return Response(
                    {
                        "message": "Contact created successfully",
                        "data": valid_request.data,
                    },
                    status=status.HTTP_201_CREATED,
                )
            except IntegrityError as e:
                return Response(
                    {"error": f"You have added {valid_request["phone_number"]} already"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(valid_request.errors, status=status.HTTP_401_UNAUTHORIZED)


class ListContactView(ListAPIView):
    """This helps list all contacts of the request user by extending the ListAPIView"""

    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="List all Contacts")
    def get(self, request: Request):
        """
        Retrieve a list of contacts added by the authenticated user.

        Args:
            request (Request): The incoming request object.

        Returns:
            Response: A Response object containing the list of contacts and a success status code.
        """
        contacts = Contact.objects.filter(user=request.user).order_by("-created_at")
        serializer = self.get_serializer(contacts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
