from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import *
from .viewsets import *


@csrf_exempt
def missing(request):
    view_set = MissingViewSet(request)
    return view_set.respond()


@csrf_exempt
def missing_id(request, pk):
    view_set = MissingIdViewSet(request, pk)
    return view_set.respond()


@csrf_exempt
def find(request):
    view_set = FindMissingViewSet(request)
    return view_set.respond()


@csrf_exempt
def profile(request):
    view_set = ProfileViewSet(request)
    return view_set.respond()


class Register(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        token = generate_token(request)
        response = Response(serializer.data)
        response.set_cookie(key="jwt", value=token, httponly=True)
        return response


@csrf_exempt
def login(request):
    view_set = LoginViewSet(request)
    return view_set.respond()


def user(request):
    view_set = UserViewSet(request)
    return view_set.respond()


@csrf_exempt
def logout(request):
    view_set = LogoutViewSet(request)
    return view_set.respond()
