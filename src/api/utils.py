import jwt
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import datetime
import json


def get_user(request):
    token = request.COOKIES.get("jwt")

    if not token:
        raise AuthenticationFailed("Unauthenticated!")

    try:
        payload = jwt.decode(token, "secret", algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed("Unauthenticated!")

    user_id = payload["id"]
    user = User.objects.filter(id=user_id).first()

    return user


def generate_token(request):
    body_unicode = request.body.decode("utf-8")
    body = json.loads(body_unicode)
    email = body["email"]
    password = body["password"]

    user = User.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationFailed("User not found!")

    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect password!")

    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, "secret", algorithm="HS256")

    return token
