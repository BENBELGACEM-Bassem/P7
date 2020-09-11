# -*- coding: utf-8 -*-
"""Main module to get adress and description for a place"""

from . import fetcher

def get_adress_for(user_request):

	google_request_instance = fetcher.GmGeoApi(user_request)
	adress = google_request_instance.get_address()
	latitude, longitude = google_request_instance.get_latitude_longitude()

	page_id = fetcher.WikiApi.get_page_id(latitude, longitude)
	location_data = fetcher.WikiApi.describe_location(page_id)


