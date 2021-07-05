from django.urls import path

from . import views

urlpatterns = [
    path("missing", views.missing, name="missing"),
    path("missing/<str:pk>", views.missing_id, name="missing_id"),
    path("find", views.find, name="find"),
    path("register", views.register, name="register"),
    path("login", views.login, name="login"),
    path("user", views.user, name="user"),
    path("logout", views.logout, name="logout"),
    path("profile", views.profile, name="profile"),
    path("result", views.get_search_result, name="result"),
]
