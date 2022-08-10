from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, LogoutView, \
    PasswordResetConfirmView, PasswordResetCompleteView, LoginView, LogoutView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, reverse

from ride.models import Passenger, TurageUser, Driver
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView


class LoginUser(LoginView):
    template_name = "registration/login.html"
    model = TurageUser
    next_page = reverse_lazy('ride-request')

class DriverRegistration(CreateView):
    template_name = "registration/driver_registration.html"
    model: Driver
    fields = "__all__"

    queryset = Driver.objects.all()
    next_page = reverse_lazy('ride-request')



