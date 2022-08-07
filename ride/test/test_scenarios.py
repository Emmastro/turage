"""
This module test real life scenarios of passengers driving requests, driver responses, 
matching riding requests, etc.
"""

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from carpool.models import Car, Driver, Passenger, Car, Edge, Waypoint, RidingRequest
from rest_framework import status

import pandas as pd


class ScenarioTests(APITestCase):

    spreadsheet = 'carpool/test/test_data/data.xlsx'

    url_passengers = reverse('passenger-list')
    url_drivers = reverse('driver-list')
    url_cars = reverse('car-list')
    url_edges = reverse('edge-list')
    mapping = [
        ('cars', url_cars, Car),
        ('drivers', url_drivers, Driver),
        ('edges', url_edges, Edge),
        ('passengers', url_passengers, Passenger),
    ]

    def setUp(self):
        return super().setUp()

    def test_load_data(self):
        """
        Tests data for each model can be loaded as expected, 
        and wrong data input returns that appropriate error based on the test cases 
        from the test spreadsheet.
        """

        for (sheet_name, url, model) in self.mapping:

            data = pd.read_excel(self.spreadsheet, sheet_name=sheet_name)
            data.fillna('', inplace=True)

            for row in data.to_dict('records'):
                response_code = row.pop('response_code')

                with self.subTest(data=data, sheet_name=sheet_name, row=row, response_code=response_code):

                    object_count = model.objects.count()
                    response = self.client.post(url, row, format='json')

                    self.assertEqual(response.status_code, response_code, msg=response.data)

                    self.assertEqual(model.objects.count(
                    ), object_count + (response_code == status.HTTP_201_CREATED),
                    msg=f'The post request for {model} failed to add an entry on the database')
