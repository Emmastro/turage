"""

shortcut: carpool.test.test_waypoints.WayPointTests.<function_name>

python manage.py test <path>

"""
import logging

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from carpool.data.initialization import init_multiple_waypoints
from carpool.test.test_data import*

from carpool.utils import get_list_from_string#, dijkstras
import pandas as pd

logging.basicConfig(level=logging.DEBUG)


class WayPointTests(APITestCase):

    url = reverse('waypoint-list')
    url_add_multiple_waypoint = reverse('waypoint-add-multiple')
    url_edge = reverse('edge-list')
    url_add_connection = reverse('waypoint-add-connection')

    def setUp(self):
        return super().setUp()

    

    def test_create_waypoint_single_not_connected_success(self):
        """
        Creates a waypoint that is not connected to any other waypoint. It essentially doesn't belong to any 
        network, and has a empty waypoints and edges attributes
        """
        data = {
            'name': "Mahogany",
            'latitude': -1,
            'longitude': 36
        }

        response = self.client.post(self.url, data, format='json')
        # TODO: check if the data was saved in the right structure
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        
    def test_create_multiple_waypoints_success(self):
        """
        Test create multiple waypoints based on the spreadsheet test data
        """
        
        response, payload = init_multiple_waypoints(self.client)
        data = response.data
        #logging.info(f"response received: {data}")
        
        id = 1
        new_payload_waypoints = []

        for waypoint in payload["waypoints"]:

            waypoint['waypoints'] = [i+1 for i in get_list_from_string(waypoint['waypoints'])]
            waypoint['edges'] = [i+1 for i in get_list_from_string(waypoint['edges'])]
           
            waypoint = {'id':id, **waypoint}
            new_payload_waypoints.append(waypoint)
            id+=1
          
           
        payload["waypoints"] = new_payload_waypoints
        
        self.assertEqual(data, payload)        


        self.assertEqual(response.status_code,
                             status.HTTP_201_CREATED)


    def test_create_multiple_waypoints_batch_success(self):
        """
        Submit all waypoints to be added as a list
        """
        pass

    def test_create_waypoint_network_test_1_success(self):
        """
        Test link driving path success
        """
        pass

    def test_create_waypoint_network_test_2_success(self):
        """
        Test link driving path success
        """
        pass
