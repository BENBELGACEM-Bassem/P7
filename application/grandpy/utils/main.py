#! /usr/bin/env python3
# coding: utf-8

"""Main module to get adress and description for a place"""

from . import fetcher


def get_data_for(user_request):
    """Get data from a user query"""
    google_request_instance = fetcher.GmGeoApi(user_request)
    adress = google_request_instance.get_address()
    latitude = google_request_instance.get_latitude_longitude()[0]
    longitude = google_request_instance.get_latitude_longitude()[1]
    page_id = fetcher.WikiApi.get_page_id(latitude, longitude)
    location_data = fetcher.WikiApi.describe_location(page_id)
    url = fetcher.WikiApi.get_url(page_id)

    return {
        'adress': adress,
        'location_data': location_data,
        'lat': latitude,
        'lng': longitude,
        'url': url}
