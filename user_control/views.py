from rest_framework.decorators import api_view  # type: ignore
from rest_framework import status  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.request import Request  # type: ignore
from user_control.tokenauth import JWTAuthentication
from .serializers import SignUpSerializer, LoginSerializer


@api_view(["POST"])
def register_user(request: Request):
    serializer = SignUpSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def login(request: Request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        token = JWTAuthentication.generate_token(payload=serializer.data)
        return Response(
            {
                "message": "Login Successful",
                "isLoggedIn": True,
                "token": token,
                "user": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_401_UNAUTHORIZED)
