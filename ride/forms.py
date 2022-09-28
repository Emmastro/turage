
from django import forms
from ride.models import RideRequest

class PassengerRideRequestForm(forms.ModelForm):

    class Meta(object):
        model = RideRequest
        fields = [ "origin_waypoint", "destination_waypoint"]
