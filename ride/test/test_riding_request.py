import logging
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase
from carpool.data.initialization import init_multiple_car, init_multiple_drivers, init_multiple_waypoints
from carpool.models import Car, Driver, Passenger, RidingRequest, Waypoint
from carpool.test.test_data import*
import pandas as pd


#from test_waypoints import test_create_multiple_waypoints_success

logging.basicConfig(level=logging.DEBUG)

class RidingRequestTest(APITestCase):

    url = reverse('ridingrequest-list')
    url_car = reverse('car-list')
    url_accept = reverse('ridingrequest-accept')
    url_waypoint = reverse('waypoint-list')
    url_drivers = reverse('driver-list')
    url_passenger = reverse('passenger-list')
    url_edges = reverse('edge-list')
    url_add_multiple_waypoint = reverse('waypoint-add-multiple')


    def test_make_riding_request_fail(self):
        pass

   
    def test_match_2_riding_requests_same_origin_destination_success(self):
        pass

    def test_fetch_address_origin_geolocation_mock(self):
        """Fetch user location with Google API (Mock)"""
        pass

    def test_fetch_address_origin_geolocation_actual(self):
        """Fetch user location with Google API (Mock)"""
        pass


    def test_make_riding_request_success(self):

        # TODO: Find a way not to have code duplicates, maybe use a decorator or utils package ...
        # THIS IS A CODE DUPLICATE FROM test_waypoints

        response_waypoint, payload_waypoint = init_multiple_waypoints(self.client)
        response_waypoint_data = response_waypoint.data
        response_cars = init_multiple_car(self.client)
        response_drivers = init_multiple_drivers(self.client)

        # create the riding request
        riding_requests = pd.read_excel(
            './carpool/test/test_data/data.xlsx', sheet_name='riding_requests')

        for row in riding_requests.to_dict('records'):
            
            # we get the index of the waypoints
            origin_waypoint_index = row['origin_waypoint']
            destination_waypoint_index = row['destination_waypoint']
            
            # using the index, given all the test waypoints were saved sequentially,
            # and the response as an ordered list maintaining the order the waypoints 
            # were saved, the index of each waypoint from the response will match the index
            # from the test dataset
            
            origorigin_waypoint_id = response_waypoint_data['waypoints'][origin_waypoint_index]['id']
            destination_waypoint_id = response_waypoint_data['waypoints'][destination_waypoint_index]['id']

            row['origin_waypoint'] = origorigin_waypoint_id
            row['destination_waypoint'] = destination_waypoint_id

            #logging.info("sending payload for riding request: %s", row)
            response = self.client.post(self.url, row, format='json')
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            #logging.info("riding request saved: response.data %s", response.data)

            #TODO: compare data sent and data received with assertEqual (handle time format)