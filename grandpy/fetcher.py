# encoding: utf-8
"""Module to retrieve data from external API's"""

import requests

from P7_02_site.grandpy.grandpyconfig import (GmgeoParams, WikiParams)

from P7_02_site.grandpy.parser import main


class GmGeoApi:
    """Class to interface with google geocode Api"""

    @staticmethod
    def fetch_gmgeo(**kwargs):
        """Get geographic data from a google geocoding Api"""
        response = requests.get(
            GmgeoParams.ENDPOINT,
            params=kwargs)
        if response.json().get('status') != 'OK':
            print("Oups ! Something went wrong," +
                  f" we have {response.json().get('status')}" +
                  " from geocoding Api")
            return None
        return response.json()

    @classmethod
    def get_address(cls):
        """Extract address from geocoding Api response"""
        # gmgeo call on parsed user question:
        geographic_coordinates = cls.fetch_gmgeo(
            address=main(), key=GmgeoParams.GMGEO_KEY)
        # Make sure we have an ok status response
        if geographic_coordinates:
            address = geographic_coordinates["results"][0].get(
                "formatted_address")
            return address

    @classmethod
    def get_latitude_longitude(cls):
        """Extract latitude coordinate from geocoding Api response"""
        # gmgeo call on parsed user question:
        geographic_coordinates = cls.fetch_gmgeo(
            address=main(), key=GmgeoParams.GMGEO_KEY)
        # Make sure we have an ok status response
        if geographic_coordinates:
            latitude = geographic_coordinates["results"][0].get(
                "geometry").get("location").get("lat")
            longitude = geographic_coordinates["results"][0].get(
                "geometry").get("location").get("lng")
            return latitude, longitude


class WikiApi:
    """Class to interface with Media wiki Api"""

    @staticmethod
    def fetch_wiki(**kwargs):
        """Get list of locations"""
        response = requests.get(
            WikiParams.ENDPOINT,
            params=kwargs)
        try:
            if response.json().get("warnings"):
                return "WikiApi_warning message: " +\
                    f" {response.json().get('warnings').get('modulename').get('*')}"
            elif response.json().get("errors"):
                return "WikiApi_error message: " +\
                    f" {(response.json().get('errors')[0].get('code'))}"
            else:
                return response.json()
        except BaseException:
            return "Something went wrong on the server side "

    @classmethod
    def get_page_id(cls, latitude, longitude):
        """Get the nearest id location from a given one"""
        # Get a list of locations around the given one
        geosearch_data = cls.fetch_wiki(
            **WikiParams.define_geosearch_params(latitude, longitude))
        # Make sure that we don't have a warning or an error
        if not isinstance((geosearch_data), str):
            # Make sure that we don't have an empty list
            if geosearch_data.get('query').get('geosearch'):
                page_id = geosearch_data.get('query').get(
                    'geosearch')[0].get('pageid')
                return page_id
            # In case of an empty list
            return 'No known location around, you may increase gradius param'
        # In case of a warning, an error or a server fail
        return geosearch_data

    @classmethod
    def describe_location(cls, page_id):
        """Get data about a known location"""
        extracted_data = cls.fetch_wiki(
            **WikiParams.define_extraction_params(page_id))
        # Make sure that we don't have a warning or an error
        if not isinstance((extracted_data), str):
            location_data = extracted_data.get('query').get(
                'pages').get(str(page_id)).get('extract')
           # Make sure 'extract' key is not related to an empty value
            if location_data != "":
                # Get only the first part of the response to avoid being long
                data_split = location_data.split('\n\n')
                return data_split[0]
            return 'No data to be extracted for this place !'
        # In case of a warning, an error or a server fail
        return extracted_data

# tests
# response = requests.get(GmgeoParams.ENDPOINT, params={'address' : main(), 'key' : GmgeoParams.GMGEO_KEY})
# print(type(response))


# addr = GmGeoApi.get_address()
# print(addr)

# lat,lon = GmGeoApi.get_latitude_longitude()
# page_id = WikiApi.get_page_id(lat,lon)
# print(page_id)
# get_location_data = WikiApi.describe_location(page_id)
# print(get_location_data)

# extracted_data = WikiApi.fetch_wiki(
#     **WikiParams.define_extraction_params(9976278))
# print(extracted_data)