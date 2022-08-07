
from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
]
