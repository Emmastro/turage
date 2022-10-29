from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from accounts.forms import DriverRegistrationForm, PassengerRegistrationForm

from ride.models import Passenger, TurageUser, Driver
from django.views.generic import CreateView


class LoginUser(LoginView):
    template_name = "registration/login.html"
    model = TurageUser
    # next_page = reverse_lazy('passenger-ride-request')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Login'
        return context
    
    def get_success_url(self):
        print("role --> ", self.request.user.role)
        if self.request.user.role == TurageUser.PASSENGER:
            return reverse_lazy('passenger-ride-request')
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Driver Registration'
        return context

    def form_valid(self, form):
        valid = super(DriverRegistration, self).form_valid(form)

        login(self.request, self.object)

        return valid


class PassengerRegistration(CreateView):
    model = Passenger
    form_class = PassengerRegistrationForm
    template_name = "registration/passenger_registration.html"

    def get_success_url(self):
        return reverse_lazy('passenger-ride-request')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["page_title"] = 'Passenger Registration'
        return context

    def form_valid(self, form):
        valid = super(PassengerRegistration, self).form_valid(form)

        login(self.request, self.object)

        return valid
