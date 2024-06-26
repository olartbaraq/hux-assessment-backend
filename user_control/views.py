from rest_framework.decorators import api_view, permission_classes  # type: ignore
from rest_framework import generics, status, permissions  # type: ignore
from rest_framework.response import Response  # type: ignore
from rest_framework.request import Request  # type: ignore
from user_control.models import BlackListedToken
from user_control.tokenauth import JWTAuthentication
from .serializers import LogoutSerializer, SignUpSerializer, LoginSerializer
from drf_yasg.utils import swagger_auto_schema  # type: ignore
from django.core.mail import EmailMultiAlternatives  # type: ignore
from django.template.loader import render_to_string  # type: ignore
from django.utils.html import strip_tags  # type: ignore
import threading


def send_mail_to_user(
    subject: str,
    from_email: str | None,
    user: str,
    recipient_list: list[str],
):
    html_message = render_to_string("content/email.html", context={"user": user})
    plain_message = strip_tags(html_message)

    message = EmailMultiAlternatives(
        subject=subject,
        body=plain_message,
        from_email=from_email,
        to=recipient_list,
    )

    message.attach_alternative(html_message, "text/html")
    message.send()


class SignUpView(generics.GenericAPIView):
    """The class that represents the sign up api view

    Args:
        generics (_type_): _description_
    """

    serializer_class = SignUpSerializer
    permission_classes: list[str] = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Create a User")
    def post(self, request: Request):
        """post method that handle the sign up request

        Args:
            request (Request): enhance a standard HttpRequest instance.
        """

        data = request.data

        # valid incoming data from client to conform with serializer
        valid_request = self.serializer_class(data=data)

        if valid_request.is_valid():
            # save user data to database
            valid_request.save()

            # Send email notification to buyer

            subject = "Welcome Aboard!!"
            from_email = None
            recipient_list = [
                valid_request.data.get("email"),  # type: ignore
            ]
            user = valid_request.data.get("name")

            # Create a new thread to send the email
            email_thread = threading.Thread(
                target=send_mail_to_user,
                args=(subject, from_email, user, recipient_list),
            )
            email_thread.start()

            response = {
                "message": "User created successfully",
                "data": valid_request.data,
            }

            return Response(data=response, status=status.HTTP_201_CREATED)
        else:
            return Response(
                data=valid_request.errors, status=status.HTTP_400_BAD_REQUEST
            )


class LoginView(generics.GenericAPIView):
    """This class represents the login api view

    Args:
        APIView (_type_): _description_
    """

    serializer_class = LoginSerializer
    permission_classes: list[str] = [permissions.AllowAny]

    @swagger_auto_schema(operation_summary="Login a User")
    def post(self, request: Request):
        """post method to authenticate the user

        Args:
            request (Request): _description_
        """

        data = request.data
        valid_request = self.serializer_class(data=data)
        if valid_request.is_valid(raise_exception=True):

            #  create a jwt token for the user using the assigned payload
            token = JWTAuthentication.generate_token(payload=valid_request.data)

            return Response(
                {
                    "message": "Login Successful",
                    "isLoggedIn": True,
                    "token": token,
                    "user": valid_request.data,
                },
                status=status.HTTP_200_OK,
            )

        return Response(valid_request.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(generics.GenericAPIView):
    """This class represents the logout api view

    Args:
        APIView (_type_): _description_
    """

    serializer_class = LogoutSerializer
    permission_classes: list[str] = [permissions.IsAuthenticated]

    @swagger_auto_schema(operation_summary="Logout a User")
    def post(self, request: Request):
        """post method to authenticate the user

        Args:
            request (Request): _description_
        """

        data = request.data
        valid_request = self.serializer_class(data=data)
        if valid_request.is_valid(raise_exception=True):

            # save the token to database and render invalid not to be used again
            blacklisted_token_obj = BlackListedToken.objects.create(
                token=valid_request.validated_data["token"], user=request.user
            )
            blacklisted_token_obj.save()
            return Response(
                {
                    "message": "User logged out successfully",
                },
                status=status.HTTP_204_NO_CONTENT,
            )

        return Response(valid_request.errors, status=status.HTTP_401_UNAUTHORIZED)
