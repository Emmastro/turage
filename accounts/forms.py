from django.contrib.auth.forms import UserCreationForm
from ride.models import Passenger, Driver


class DriverRegistrationForm(UserCreationForm):

    class Meta(object):

        model = Driver
        fields = ["username", "first_name", "last_name", "email", "gender",
                  "country", "national_id", "phone_number", "driver_license"]


<<<<<<< HEAD
class PassengerRegistrationForm(UserCreationForm):

    class Meta(object):
        model = Passenger
        fields = ["username", "first_name", "last_name", "email",
                  "gender", "country", "university", "phone_number"]

=======
        if commit:
            driver.save()
        return driver

class PassengerRegistrationForm(forms.ModelForm):

    class Meta(object):
        model = Passenger
        fields = ["first_name", "last_name", "email", "gender",  "username", "password" , "country", "university", "phone_number"]

    def save(self, commit=True):
        passenger = super().save(commit=False)
        passenger.set_password(self.cleaned_data['password'])

        if commit:
            passenger.save()
<<<<<<< HEAD
        return passenger
>>>>>>> 193c23f (Passenger Registration)
=======
        return passenger
>>>>>>> b3eb8ba (Passenger Registration)
