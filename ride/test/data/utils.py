"""
This module contains utility functions for data management
"""
import pandas as pd

import googlemaps

import gmaps

import os
from dotenv import load_dotenv

load_dotenv()

gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAP_API_KEY'))

def parse_geocode_response(address: str):
    """
    parse address from google maps api response
    """

    geocode_result = gmaps.geocode(address)
    geocode_result_len = len(geocode_result)
    if geocode_result_len >= 1:
        data = {
        'longitude':geocode_result[0]['geometry']['location']['lng'],
        'latitude':geocode_result[0]['geometry']['location']['lat'],
        'formatted_address': geocode_result[0]['formatted_address'],
        'full_details': geocode_result,
        'success_geocode': True,
        'match_found_geocode': geocode_result_len
        }
        
    elif geocode_result_len == 0:
        # Address could not be found?
        data = {'error':'No response', 'success_geocode': True, 'full_details': geocode_result}

    return data


def parse_distance_matrix_response(origins, destinations, id):
    """
    parse google maps api response
    """
    # TODO: include transit
    directions_result = gmaps.directions(origins, destinations)
    directions_result_len = len(directions_result)

    if directions_result_len >= 1:

        data = {
            'id': id,
            'distance': directions_result[0]['legs'][0]['distance']['value'], # in km
            'duration': directions_result[0]['legs'][0]['duration']['value'], # in seconds
            'full_direction_details': directions_result,
            'success_distance_matrix': True,
            'match_found_distance_matrix': directions_result_len,
        }
    else:
        data = {
            'id':id,
            'error':'No response',
            'success_distance_matrix': False,
            'full_direction_details': directions_result
        }

    return data
