from rest_framework import serializers  # type: ignore
from .models import Contact


class ContactSerializer(serializers.ModelSerializer):
    """
    This class implements the serializer interface to perform crud
    operations on contacts by extending the model serializer class

    Args:
        serializers (class): helps turn database columns to json fields to be interacted with

    """

    class Meta:
        model = Contact
        fields = ["lastname", "firstname", "phone_number"]
        read_only_fields = ("id", "created_at", "updated_at")
