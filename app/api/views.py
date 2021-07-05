from django.views.decorators.csrf import csrf_exempt
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


@csrf_exempt
def register(request):
    view_set = RegisterViewSet(request)
    return view_set.respond()


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


@csrf_exempt
def get_search_result(request):
    view_set = ResultViewSet(request)
    return view_set.respond()
