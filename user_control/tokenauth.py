import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from rest_framework.authentication import BaseAuthentication  # type: ignore
from rest_framework.exceptions import AuthenticationFailed  # type: ignore
from django.conf import settings  # type: ignore
from django.contrib.auth import get_user_model  # type: ignore
from datetime import datetime, timedelta, timezone

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = self.extract_token(request=request)
        if token is None:
            return None

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            self.verify_token(payload=payload)

            user_id = payload["id"]
            user = User.objects.get(id=user_id)
            return (user, None)
        except (InvalidTokenError, ExpiredSignatureError, User.DoesNotExist):
            raise AuthenticationFailed("Invalid Token")

    def verify_token(self, payload):
        # Check if the token has an expiration time
        if "exp" not in payload:
            raise InvalidTokenError("no expiration token, Invalid")

        # Get the expiration timestamp from the payload
        exp_timestamp = payload["exp"]

        # Get the current UTC timestamp
        current_timestamp = datetime.now(tz=timezone.utc).timestamp()

        # Check if the token has expired
        if current_timestamp > exp_timestamp:
            raise ExpiredSignatureError("Token has expired")

    def extract_token(self, request):
        # Get the Authorization header from the request
        auth_header = request.headers.get("Authorization")

        # Check if the header starts with "Bearer "
        if auth_header and auth_header.startswith("Bearer "):
            return auth_header.split(" ")[1]
        return None

    @staticmethod
    def generate_token(payload):
        # Set the expiration time for the token (1 hour from now)
        expiration = datetime.now(tz=timezone.utc) + timedelta(hours=1)
        payload["exp"] = expiration

        # Create the JWT token
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm="HS256")
        return token
