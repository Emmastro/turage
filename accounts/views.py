from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, LogoutView, \
    PasswordResetConfirmView, PasswordResetCompleteView, LoginView, LogoutView
from django.urls import reverse_lazy

from ride.models import Passenger, TurageUser


class LoginUser(LoginView):
    template_name = "registration/login.html"
    model = TurageUser
    next_page = reverse_lazy('ride-request')