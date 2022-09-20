


from django import forms
from ride.models import Passenger, TurageUser, Driver
from django.contrib.auth.hashers import make_password

class DriverRegistrationForm(forms.ModelForm):

    class Meta(object):
        model = Driver
        fields = ["first_name", "last_name", "email", "gender",  "username", "password" , "country", "national_id", "phone_number", "driver_license"]

    def save(self, commit=True):
        driver = super().save(commit=False)
        driver.set_password(self.cleaned_data['password'])

        if commit:
            driver.save()
        return driver