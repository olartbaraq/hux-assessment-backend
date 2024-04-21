from rest_framework import serializers  # type: ignore
from django.contrib.auth import get_user_model, authenticate  # type: ignore


class SignUpSerializer(serializers.ModelSerializer):
    """This class implements the interface DRF will use to serve the sign up variables in the api

    Args:
        serializers (_type_): _description_
    """

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(  # type: ignore
            email=validated_data["email"],
            name=validated_data["name"],
            password=validated_data["password"],
        )
        return user


class LoginSerializer(serializers.Serializer):
    """_summary_

    Args:
        serializers (_type_): _description_
    """

    email = serializers.EmailField()
    name = serializers.CharField(read_only=True)
    id = serializers.CharField(max_length=15, read_only=True)
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get("email", None)
        password = data.get("password", None)

        if email is None:
            raise serializers.ValidationError("Email is required")

        if password is None:
            raise serializers.ValidationError("Password is required")

        user = authenticate(username=email, password=password)

        if user is None:
            raise serializers.ValidationError("Invalid Email or Password")

        if not user.is_active:
            raise serializers.ValidationError("User is inactive")

        return {
            "email": user.email,  # type: ignore
            "id": user.id,  # type: ignore
            "name": user.name,  # type: ignore
        }


class LogoutSerializer(serializers.Serializer):
    token = serializers.CharField(write_only=True)
