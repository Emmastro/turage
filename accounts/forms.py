


from django import forms
from ride.models import Passenger, TurageUser, Driver


class DriverRegistrationForm(forms.ModelForm):

    class Meta(object):
        model = Driver

        exclude = ('')