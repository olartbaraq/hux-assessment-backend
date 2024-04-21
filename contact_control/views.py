from rest_framework import viewsets  # type: ignore
from .serializers import Contact, ContactSerializer
from rest_framework.permissions import IsAuthenticated  # type: ignore


class ContactViewSet(viewsets.ModelViewSet):
    """this helps create list, get, update, delete views by extending the viewset class"""

    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [IsAuthenticated]
