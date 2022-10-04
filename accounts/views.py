from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
<<<<<<< HEAD
from accounts.forms import DriverRegistrationForm, PassengerRegistrationForm
from django.core.mail import send_mail
=======
from django.shortcuts import render, redirect, reverse
from accounts.forms import DriverRegistrationForm, PassengerRegistrationForm
>>>>>>> 193c23f (Passenger Registration)

from ride.models import Passenger, TurageUser, Driver
from django.views.generic import CreateView


class LoginUser(LoginView):
    template_name = "registration/login.html"
    model = TurageUser

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Login'
        return context
    
    def get_success_url(self):

        if self.request.user.role == TurageUser.PASSENGER:
            return reverse_lazy('ride-request')
        elif self.request.user.role == TurageUser.DRIVER:
            return reverse_lazy('ride-request-near')


class LogoutUser(LogoutView):
    next_page = reverse_lazy('login')


class DriverRegistration(CreateView):
    model = Driver
    form_class = DriverRegistrationForm
    template_name = "registration/driver_registration.html"

    def get_success_url(self):
        return reverse_lazy('ride-request-near')

<<<<<<< HEAD
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Driver Registration'
        return context
=======
class PassengerRegistration(CreateView):
    model = Passenger
    form_class = PassengerRegistrationForm
    template_name= "registration/passenger_registration.html"

    def get_success_url(self):
        return reverse_lazy('ride-request-near')

>>>>>>> 193c23f (Passenger Registration)

    def form_valid(self, form):
        valid = super(DriverRegistration, self).form_valid(form)

        # TODO: set email content as template, and separate them from the python code
        send_mail(
            "Welcome to Turage",
            "You have successfully registered as a driver",
            "info@turagerides.com",
            [self.object.email])
        login(self.request, self.object)

        return valid


class PassengerRegistration(CreateView):
    model = Passenger
    form_class = PassengerRegistrationForm
    template_name = "registration/passenger_registration.html"

    def get_success_url(self):
        return reverse_lazy('ride-request')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Passenger Registration'
        return context

    def form_valid(self, form):
        valid = super(PassengerRegistration, self).form_valid(form)
        
        send_mail(
            "Welcome to Turage", "You have successfully registered as a passenger", 
            "info@turagerides.com",
            [self.object.email])
        login(self.request, self.object)

        return valid
