
from django.urls import path

from . import views

urlpatterns = [
    #path("", views.index, name="index"),
    path("login/", views.LoginUser.as_view(), name="login"),
    path("logout/", views.LogoutUser.as_view(), name="logout"),
    path("registration/driver", views.DriverRegistration.as_view(), name="driver_registration"),
    path("registration/passenger", views.PassengerRegistration.as_view(), name="passenger_registration")
]
