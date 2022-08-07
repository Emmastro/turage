import imp

"""
This module contains utility functions for database initialization
"""

import pandas as pd
from django.urls import reverse

url_add_multiple_waypoint = reverse('waypoint-add-multiple')
url_car = reverse('car-list')
url_drivers = reverse('driver-list')
url_passenger = reverse('passenger-list')

edges = pd.read_excel('./carpool/test/test_data/data.xlsx', sheet_name='edges')
waypoints = pd.read_excel('./carpool/test/test_data/data.xlsx', sheet_name='waypoints')

cars = pd.read_excel('./carpool/test/test_data/data.xlsx', sheet_name='cars')


def init_multiple_waypoints(client, edges=edges, waypoints=waypoints):
    """
    Initialize multiple waypoints on a single request based on the test data
    """

    edges_fields = edges[['distance']] 
    waypoints_fields = waypoints[['name', 'waypoints', 'edges','longitude', 'latitude',]]
    
    payload = {
        'waypoints': waypoints_fields.to_dict('records'),
        'edges': edges_fields.to_dict('records')            
    }
    
    response = client.post(
        url_add_multiple_waypoint, payload, format='json')
    
    return response, payload

def init_multiple_car(client):
    """
    Initialize multiple cars on a single request based on the test data
    """

    cars = pd.read_excel(
        './carpool/test/test_data/data.xlsx', sheet_name='cars')
    
    cars.fillna("", inplace=True)

    response = []
    for row in cars.to_dict('records'):
        if row['plate_number'] != "":
            row['plate_number'] = int(row['plate_number'])
        row.pop('response_code')
        row.pop('id')
        response.append(client.post(url_car, row, format='json'))

    return response


def init_multiple_drivers(client):
    """
    Initialize multiple drivers on a single request based on the test data
    """
    pass

    drivers = pd.read_excel(
        './carpool/test/test_data/data.xlsx', sheet_name='drivers')

    drivers.fillna("", inplace=True)
    response = []
    for row in drivers.to_dict('records'):

        row.pop('response_code')

        response.append(client.post(url_drivers, row, format='json'))
    return response

def init_multiple_passengers(client):
    passengers = pd.read_excel(
            './carpool/test/test_data/data.xlsx', sheet_name='passengers')
    passengers.fillna("", inplace=True)
    
    response = []
    for row in passengers.to_dict('records'):
        row.pop('response_code')
        response.append(client.post(url_passenger, row, format='json'))

    return response
