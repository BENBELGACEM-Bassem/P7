#! /usr/bin/env python3
# coding: utf-8

"""Module to retrieve data from external API's"""

import requests

from .config import (GmgeoParams, WikiParams)

from .parser import parse


class GmGeoApi:
    """Class to interface with google geocode Api"""

    def __init__(self, user_query):
        self.user_query = user_query

    @staticmethod
    def fetch_gmgeo(**kwargs):
        """Get geographic data from a google geocoding Api"""
        response = requests.get(
            GmgeoParams.ENDPOINT,
            params=kwargs)
        # Managing non ok status, for debugging purpose
        try:
            if response.json().get('status') != 'OK':
                return ("Oups ! Something went wrong," +
                        f" we have {response.json().get('status')}" +
                        " from geocoding Api")
            else:
                return response.json()

        except BaseException:
            return "Something went wrong on the network connexion "

    def get_address(self):
        """Extract address from geocoding Api response"""
        # gmgeo call on parsed user question:
        geographic_coordinates = GmGeoApi.fetch_gmgeo(
            address=parse(self.user_query), key=GmgeoParams.GMGEO_KEY)
        # Make sure we have an ok status response
        if not isinstance((geographic_coordinates), str):
            address = geographic_coordinates["results"][0].get(
                "formatted_address")
            if address != "":
                return address
        return None

    def get_latitude_longitude(self):
        """Extract latitude coordinate from geocoding Api response"""
        # gmgeo call on parsed user question:
        geographic_coordinates = GmGeoApi.fetch_gmgeo(
            address=parse(self.user_query), key=GmgeoParams.GMGEO_KEY)
        # Make sure we have an ok status response
        if not isinstance((geographic_coordinates), str):
            latitude = geographic_coordinates["results"][0].get(
                "geometry").get("location").get("lat")
            longitude = geographic_coordinates["results"][0].get(
                "geometry").get("location").get("lng")
            if latitude != "" and longitude != "":
                return latitude, longitude
        return None


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
                return "WikiApi_warning message: " + \
                    f" {response.json().get('warnings').get('modulename').get('*')}"
            elif response.json().get("errors"):
                return "WikiApi_error message: " + \
                    f" {(response.json().get('errors')[0].get('code'))}"
            else:
                return response.json()
        except BaseException:
            return "Something went wrong on the network connexion "

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
                return location_data
            return 'No data to be extracted for this place !'
        # In case of a warning, an error a server fail or connection off
        return extracted_data

    @classmethod
    def get_url(cls, page_id):
        """Get a wikipedia link for the location"""
        extracted_data = cls.fetch_wiki(
            **WikiParams.define_extraction_params(page_id))
        # Make sure that we don't have a warning or an error
        if not isinstance((extracted_data), str):
            url = extracted_data.get('query').get(
                'pages').get(str(page_id)).get('fullurl')
            # Make sure 'url' key is not related to an empty value
            if url != "":
                return url
            return 'No url to be extracted for this place !'
        # In case of a warning, an error, a server fail or connection off
        return extracted_data
