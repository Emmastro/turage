from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, LogoutView, \
    PasswordResetConfirmView, PasswordResetCompleteView, LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse
from accounts.forms import DriverRegistrationForm

from ride.models import Passenger, TurageUser, Driver
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class LoginUser(LoginView):
    template_name = "registration/login.html"
    model = TurageUser
    next_page = reverse_lazy('ride-request')

class DriverRegistration(CreateView):
    model= Driver
    form_class = DriverRegistrationForm
    template_name= "registration/driver_registration.html"

    def get_success_url(self):
        return reverse_lazy('login')

 

