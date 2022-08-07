import logging

from django.urls import reverse

from rest_framework import status
from rest_framework.decorators import authentication_classes
from rest_framework.generics import ListAPIView
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import RefreshToken


from carpool.models import Car, Driver, Passenger, Car
from carpool.test.test_data import *

import pytest 


class AuthenticationTests(APITestCase):
    url = reverse('token_obtain_pair')
    @pytest.fixture
    def api_client():
        # TODO: use passenger data from the test data spreadsheet
        user = None #Passenger.objects.create_user(**PASSENGER_1)
        logging.info(user)
        client = APIClient()
        refresh = RefreshToken.for_user(user)
        client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        return client

    def test_authenticate_passenger_success(self):
        pass



            # authenticate 
            
            

    def test_authenticate_passenger_fail(self):
            pass

    def test_authenticated_driver_accept_driving_request(self):
            pass

    def test_authenticated_driver_accept_driving_request_fail(self):
            pass

    def test_non_authenticated_driver_accept_driving_request_fail(self):
            pass

    def test_create_driver_fail(self):
            pass

    def test_create_driver_with_riding_path(self):
            pass
