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

            contact_obj = Contact.objects.create(
                firstname=valid_request["firstname"],
                lastname=valid_request["lastname"],
                phone_number=valid_request["phone_number"],
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

        return Response(valid_request.errors, status=status.HTTP_401_UNAUTHORIZED)


class ListContactView(ListAPIView):
    """this helps list all contacts of the request user by extending the CreateAPIView post method"""

    serializer_class = ContactSerializer
    permission_classes: list[str] = [IsAuthenticated]

    @swagger_auto_schema(operation_summary="List all Contacts")
    def post(self, request: Request):
        """post method to create a contact

        Args:
            request (Request): _description_
        """

        data = request.data
        user = request.user
        valid_request = self.serializer_class(data=data)
        if valid_request.is_valid(raise_exception=True):

            contact_obj = Contact.objects.create(
                firstname=valid_request["firstname"],
                lastname=valid_request["lastname"],
                phone_number=valid_request["phone_number"],
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

        return Response(valid_request.errors, status=status.HTTP_401_UNAUTHORIZED)
