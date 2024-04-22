from django.db import IntegrityError  # type: ignore
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView # type: ignore
from .serializers import Contact, ContactSerializer
from rest_framework.permissions import IsAuthenticated  # type: ignore
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.request import Request  # type: ignore
from rest_framework import status  # type: ignore
from django.shortcuts import get_object_or_404  # type: ignore


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


class UpdateContactView(UpdateAPIView):
    """This helps update an existing contact by extending the UpdateAPIView"""
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Update a Contact")
    def put(self, request: Request, pk:int):
        """
        Update an existing contact for the authenticated user.

        Args:
            request (Request): The incoming request object.
            pk (int): The primary key of the contact to be updated.

        Returns:
            Response: A Response object containing the updated contact and a success status code.
        """
        contact = get_object_or_404(Contact, pk=pk, user=request.user)
        serializer = self.serializer_class(contact, data=request.data, partial=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class RetrieveContactView(RetrieveAPIView):
    """This helps get an existing contact by extending the RetrieveAPIView"""
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="Get a Contact")
    def get(self, request: Request, pk:int):
        """
        Get an existing contact for the authenticated user.

        Args:
            request (Request): The incoming request object.
            pk (int): The primary key of the contact to be updated.

        Returns:
            Response: A Response object containing the updated contact and a success status code.
        """
        contact = get_object_or_404(Contact, pk=pk, user=request.user)
        serializer = self.get_serializer(contact)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class DeleteContactView(DestroyAPIView):
    """This helps delete an existing contact by extending the RetrieveAPIView"""
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]


    @swagger_auto_schema(operation_summary="Delete a Contact")
    def delete(self, request: Request, pk:int):
        """
        Delete an existing contact for the authenticated user.

        Args:
            request (Request): The incoming request object.
            pk (int): The primary key of the contact to be deleted.

        Returns:
            Response: A Response object with a success message and a success status code.
        """
        contact = get_object_or_404(Contact, pk=pk, user=request.user)
        contact.delete()
        return Response({"message": "Contact deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
