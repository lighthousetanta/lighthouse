from ..models import *
from ..utils import *
from django.http import JsonResponse
from .base import BaseViewSet
from rest_framework.exceptions import AuthenticationFailed
import json
from django.db import IntegrityError


class RegisterViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.verbs = {"POST": self.post}

    def post(self):
        try:
            body_unicode = self.request.body.decode("utf-8")
            body = json.loads(body_unicode)
            password = body.pop("password", None)
            user = User(**body)
            user.set_password(password)
            user.save()
            token, user = generate_token(self.request)
            response = JsonResponse(user.serialize())
            response.set_cookie(key="jwt", value=token, httponly=True)
            return response
        except IntegrityError as e:
            return JsonResponse({"message": "username taken"})


class LoginViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.verbs = {"POST": self.post}

    def post(self):
        try:
            token, user = generate_token(self.request)
            response = JsonResponse(user.serialize())
            response.set_cookie(key="jwt", value=token, httponly=True)
            return response
        except AuthenticationFailed as e:
            return JsonResponse({"message": str(e)})


class ProfileViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.verbs = {"GET": self.get}

    def get(self):
        user = get_user(self.request)
        reported_cases = KnownMissingPerson.objects.filter(contactPerson=user).all()
        reported_cases = [case.serialize() for case in reported_cases]
        return JsonResponse(reported_cases, safe=False)


class UserViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.verbs = {"GET": self.get}

    def get(self):
        user = get_user(self.request)
        return JsonResponse(user.serialize())


class LogoutViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.verbs = {"POST": self.post}

    def post(self):
        response = JsonResponse({})
        response.delete_cookie("jwt")
        response.data = {"message": "success"}
        return response
