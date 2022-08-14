
from django.urls import path

from . import views

urlpatterns = [
    path("ride/request/", views.RideRequestView.as_view(), name="ride-request"),
    path("ride/request-near/", views.RideRequestNearView.as_view(), name="ride-request-near"),
    path("ride/passenger-request", views.PassengerRideRequestView.as_view(), name="Passenger-ride-request"),
    path('', views.home, name='home'),
]

