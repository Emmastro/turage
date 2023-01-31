from django.contrib.auth.forms import UserCreationForm
from ride.models import Passenger, Driver


class DriverRegistrationForm(UserCreationForm):

    class Meta(object):

        model = Driver
        fields = ["username", "first_name", "last_name", "email", "gender",
                  "country", "national_id", "phone_number", "driver_license"]

class PassengerRegistrationForm(UserCreationForm):

    class Meta(object):
        model = Passenger
        fields = ["username", "first_name", "last_name", "email",
                  "gender", "country", "university", "phone_number"]

    def save(self, commit=True):
        passenger = super().save(commit=False)
        passenger.set_password(self.cleaned_data['password'])

        if commit:
            passenger.save()

