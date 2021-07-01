from ..models import *
from ..utils import *
from django.http import JsonResponse
from .base import BaseViewSet


class RegisterViewSet(BaseViewSet):
    def __int__(self, request):
        super().__init__(request)
        self.verbs = {"POST": self.post}

    def post(self):
        pass


class LoginViewSet(BaseViewSet):
    def __init__(self, request):
        super().__init__(request)
        self.verbs = {"POST": self.post}

    def post(self):
        token = generate_token(self.request)
        response = JsonResponse({})
        response.set_cookie(key="jwt", value=token, httponly=True)
        return response


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
