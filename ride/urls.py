
from django.urls import path

from . import views

urlpatterns = [
    path("ride/request/", views.RideRequestView.as_view(), name="ride-request"),
    path("ride/request-near/", views.RideRequestNearView.as_view(), name="ride-request-near"),
    path("ride/request-near/<int:pk>/", views.RideRequestNearDetailView.as_view(), name="ride-request-near-detail"),
    path("ride/my-requests/", views.MyRequestsView.as_view(), name="my-requests"),
    path("ride/my-requests/<int:pk>", views.MyRequestsDetailView.as_view(), name="my-requests-detail"),
    path("ride/passenger-request", views.PassengerRideRequestView.as_view(), name="passenger-ride-request"),
    path('', views.home, name='home'),
    path('automotive', views.automotive, name='automotive'),
]

