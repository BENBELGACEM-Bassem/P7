""" Module for testing fetcher module"""


import pytest

import requests

from P7_02_site.grandpy.grandpyconfig import (Scrap, GmgeoParams, WikiParams)

from P7_02_site.grandpy.parser import main

from P7_02_site.grandpy.fetcher import(GmGeoApi, WikiApi)


GMGEO_OK = {"results": [{"address_components": [{"long_name": "1600",
                                                 "short_name": "1600",
                                                 "types": ["street_number"]},
                                                {"long_name": "Amphitheatre Pkwy",
                                                 "short_name": "Amphitheatre Pkwy",
                                                 "types": ["route"]},
                                                {"long_name": "Mountain View",
                                                 "short_name": "Mountain View",
                                                 "types": ["locality",
                                                           "political"]},
                                                {"long_name": "Santa Clara County",
                                                 "short_name": "Santa Clara County",
                                                 "types": ["administrative_area_level_2",
                                                           "political"]},
                                                {"long_name": "California",
                                                 "short_name": "CA",
                                                 "types": ["administrative_area_level_1",
                                                           "political"]},
                                                {"long_name": "United States",
                                                 "short_name": "US",
                                                 "types": ["country",
                                                           "political"]},
                                                {"long_name": "94043",
                                                 "short_name": "94043",
                                                 "types": ["postal_code"]}],
                         "formatted_address": "1600 Amphitheatre Parkway, Mountain View, CA 94043, USA",
                         "geometry": {"location": {"lat": 37.4224764,
                                                   "lng": -122.0842499},
                                      "location_type": "ROOFTOP",
                                      "viewport": {"northeast": {"lat": 37.4238253802915,
                                                                 "lng": -122.0829009197085},
                                                   "southwest": {"lat": 37.4211274197085,
                                                                 "lng": -122.0855988802915}}},
                         "place_id": "ChIJ2eUgeAK6j4ARbn5u_wAGqWA",
                         "plus_code": {"compound_code": "CWC8+W5 Mountain View, California, United States",
                                       "global_code": "849VCWC8+W5"},
                         "types": ["street_address"]}],
            "status": "OK"}

GMGEO_KO = {
    "results": [],
    "status": "ZERO_RESULTS"
}

WIKI_OK_LOCATIONS = {'batchcomplete': '',
                     'query': {'geosearch': [{'dist': 129.9,
                                              'lat': 37.78785,
                                              'lon': -122.40065,
                                              'ns': 0,
                                              'pageid': 6422233,
                                              'primary': '',
                                              'title': 'Academy of Art University'},
                                             {'dist': 140.9,
                                              'lat': 37.788139,
                                              'lon': -122.399056,
                                              'ns': 0,
                                              'pageid': 5105544,
                                              'primary': '',
                                              'title': '101 Second Street'},
                                             {'dist': 163.4,
                                              'lat': 37.7858,
                                              'lon': -122.4008,
                                              'ns': 0,
                                              'pageid': 429553,
                                              'primary': '',
                                              'title': "Musée d'Art moderne de San Francisco"},
                                             {'dist': 244.1,
                                              'lat': 37.789062,
                                              'lon': -122.398831,
                                              'ns': 0,
                                              'pageid': 2350884,
                                              'primary': '',
                                              'title': 'Golden Gate University'},
                                             {'dist': 268.7,
                                              'lat': 37.7854,
                                              'lon': -122.402,
                                              'ns': 0,
                                              'pageid': 4644434,
                                              'primary': '',
                                              'title': 'Yerba Buena Center for the Arts'},
                                             {'dist': 338,
                                              'lat': 37.79,
                                              'lon': -122.4,
                                              'ns': 0,
                                              'pageid': 3405328,
                                              'primary': '',
                                              'title': 'Liste des plus hautes constructions de San '
                                              'Francisco'},
                                             {'dist': 369.6,
                                              'lat': 37.7842,
                                              'lon': -122.402,
                                              'ns': 0,
                                              'pageid': 3935225,
                                              'primary': '',
                                              'title': 'Moscone Center'},
                                             {'dist': 384.3,
                                              'lat': 37.7903,
                                              'lon': -122.3985,
                                              'ns': 0,
                                              'pageid': 11091020,
                                              'primary': '',
                                              'title': 'Oceanwide Center'},
                                             {'dist': 384.7,
                                              'lat': 37.788688,
                                              'lon': -122.403477,
                                              'ns': 0,
                                              'pageid': 9025323,
                                              'primary': '',
                                              'title': '88 Kearny Street'},
                                             {'dist': 401.6,
                                              'lat': 37.7858,
                                              'lon': -122.404,
                                              'ns': 0,
                                              'pageid': 9902380,
                                              'primary': '',
                                              'title': 'Contemporary Jewish Museum'}]}}

WIKI_KO_LOCATIONS = {'batchcomplete': '', 'query': {'geosearch': []}}

WIKI_WARNINGS_RESPONSE = {
    'batchcomplete': '', 'query': {'geosearch': ['this is a mock']},
    "warnings": {
        "modulename": {
            "*": "warning text"}
    }
}

WIKI_ERROR_RESPONSE = {
    "batchcomplete": "", "query": {"geosearch": ['this is a mock']},
    "errors": [{"code": "error-code",
                "data": "[...any extra data...]",
                "module": "path to the API module that generated the error"
                },
               ],
    "docref": "human-readable message on where to find help"
}

WIKI_OK_DESCRIPTION = {
    'batchcomplete': '',
    'query': {
        'pages': {
            '9976278': {
                'pageid': 9976278,
                'ns': 0,
                'title': 'Place de la République (Tunis)',
                'extract': "La place de la République (arabe : ساحة الجمهورية) est une place de Tunis, capitale de la Tunisie.\n\n\n== Situation et accès ==\nLa place de la République est située à l'intersection de la Liberté, de l'avenue du Ghana, de la rue Jebel-el-Fath, de l'avenue de Paris, de l'avenue Habib-Thameur, de la rue du Parc et de l'avenue de Londres.\nLe jardin Habib-Thameur se trouve à son angle sud-ouest.\nElle est desservie par la station de métro République. \n\n\n== Origine du nom ==\nLa place commémore la proclamation de la République, le 24 juillet 1957.\nLa place porte le nom de l'écrivain français Anatole France sous la période du protectorat français.\nCette place a également été connue sous le nom de « Passage », qu'on utilise encore souvent de nos jours.\n\n\n== Historique ==\n\nLa place constitue dès sa création un nœud ferroviaire important. En effet, plusieurs lignes de tramways y passent, ainsi que la branche Nord du TGM, jusqu'au démantèlement de toutes ces lignes de la Compagnie des tramways de Tunis dans les années 1960. La place accueille alors également la gare de Tunis-Nord, disparue en 1965.\nAvec la création de la ligne 2 du métro léger en 1989, l'emplacement de cette gare est désormais occupé par…",
                'contentmodel': 'wikitext',
                'pagelanguage': 'fr',
                'pagelanguagehtmlcode': 'fr',
                'pagelanguagedir': 'ltr',
                'touched': '2020-08-21T08:45:19Z',
                'lastrevid': 168801661,
                'length': 3778,
                'fullurl': 'https://fr.wikipedia.org/wiki/Place_de_la_R%C3%A9publique_(Tunis)',
                'editurl': 'https://fr.wikipedia.org/w/index.php?title=Place_de_la_R%C3%A9publique_(Tunis)&action=edit',
                'canonicalurl': 'https://fr.wikipedia.org/wiki/Place_de_la_R%C3%A9publique_(Tunis)'}}}}
WIKI_KO_DESCRIPTION = {
    'batchcomplete': '',
    'query': {
        'pages': {
            '9976278': {
                'pageid': 9976278,
                'ns': 0,
                'title': 'Somewhere',
                'extract': "",
                'contentmodel': 'wikitext',
                'pagelanguage': 'fr',
                'pagelanguagehtmlcode': 'fr',
                'pagelanguagedir': 'ltr',
                'touched': '2020-08-21T08:45:19Z',
                'lastrevid': 168801661,
                'length': 3778,
                'fullurl': 'https://fr.wikipedia.org/wiki/Place_de_la_R%C3%A9publique_(Tunis)',
                'editurl': 'https://fr.wikipedia.org/w/index.php?title=Place_de_la_R%C3%A9publique_(Tunis)&action=edit',
                'canonicalurl': 'https://fr.wikipedia.org/wiki/Place_de_la_R%C3%A9publique_(Tunis)'}}}}


@pytest.fixture
def mock_gmgeo_ok_status(monkeypatch):
    def mock_requests(url, params):
        class Response:
            def json(self):
                return GMGEO_OK
        return Response()
    monkeypatch.setattr(requests, 'get', mock_requests)


@pytest.fixture
def mock_gmgeo_ko_status(monkeypatch):
    def mock_requests(url, params):
        class Response:
            def json(self):
                return GMGEO_KO
        return Response()
    monkeypatch.setattr(requests, 'get', mock_requests)


@pytest.fixture
def mock_wiki_ok_locations(monkeypatch):
    def mock_requests(url, params):
        class Response:
            def json(self):
                return WIKI_OK_LOCATIONS
        return Response()
    monkeypatch.setattr(requests, 'get', mock_requests)


@pytest.fixture
def mock_wiki_ko_locations(monkeypatch):
    def mock_requests(url, params):
        class Response:
            def json(self):
                return WIKI_KO_LOCATIONS
        return Response()
    monkeypatch.setattr(requests, 'get', mock_requests)


@pytest.fixture
def mock_wiki_warning(monkeypatch):
    def mock_requests(url, params):
        class Response:
            def json(self):
                return WIKI_WARNINGS_RESPONSE
        return Response()
    monkeypatch.setattr(requests, 'get', mock_requests)


@pytest.fixture
def mock_wiki_error(monkeypatch):
    def mock_requests(url, params):
        class Response:
            def json(self):
                return WIKI_ERROR_RESPONSE
        return Response()
    monkeypatch.setattr(requests, 'get', mock_requests)


@pytest.fixture
def mock_wiki_ok_description(monkeypatch):
    def mock_requests(url, params):
        class Response:
            def json(self):
                return WIKI_OK_DESCRIPTION
        return Response()
    monkeypatch.setattr(requests, 'get', mock_requests)


@pytest.fixture
def mock_wiki_ko_description(monkeypatch):
    def mock_requests(url, params):
        class Response:
            def json(self):
                return WIKI_KO_DESCRIPTION
        return Response()
    monkeypatch.setattr(requests, 'get', mock_requests)


def test_get_adress_with_ok_status(mock_gmgeo_ok_status):
    address = GmGeoApi.get_address()
    assert address == GMGEO_OK["results"][0].get("formatted_address")


def test_get_adress_with_ko_status(mock_gmgeo_ko_status):
    address = GmGeoApi.get_address()
    assert address is None


def test_get_latitude_longitude_with_ok_status(mock_gmgeo_ok_status):
    gps_coordinates = GmGeoApi.get_latitude_longitude()
    assert gps_coordinates == (
        GMGEO_OK["results"][0].get("geometry").get("location").get("lat"),
        GMGEO_OK["results"][0].get("geometry").get("location").get("lng"))


def test_get_latitude_longitude_with_ko_status(mock_gmgeo_ko_status):
    gps_coordinates = GmGeoApi.get_latitude_longitude()
    assert gps_coordinates is None


def test_get_page_id_with_successful_response(mock_wiki_ok_locations):
    locations = WikiApi.get_page_id(37.4224764, -122.0842499)
    assert locations == WIKI_OK_LOCATIONS.get(
        'query').get('geosearch')[0].get('pageid')


def test_get_page_id_with_empty_response(mock_wiki_ko_locations):
    locations = WikiApi.get_page_id(37.4224764, -122.0842499)
    assert locations == 'No known location around, you may increase gradius param'


def test_get_page_id_with_warning_response(mock_wiki_warning):
    locations = WikiApi.get_page_id(37.4224764, -122.0842499)
    assert locations == "WikiApi_warning message: " +\
        f" {WIKI_WARNINGS_RESPONSE.get('warnings').get('modulename').get('*')}"


def test_get_page_id_with_error_response(mock_wiki_error):
    locations = WikiApi.get_page_id(37.4224764, -122.0842499)
    assert locations == "WikiApi_error message: " +\
        f" {(WIKI_ERROR_RESPONSE.get('errors')[0].get('code'))}"


def test_describe_location_with_warning_response(mock_wiki_warning):
    description = WikiApi.describe_location(6422233)
    assert description == "WikiApi_warning message: " +\
        f" {WIKI_WARNINGS_RESPONSE.get('warnings').get('modulename').get('*')}"


def test_describe_location_with_error_response(mock_wiki_error):
    description = WikiApi.describe_location(6422233)
    assert description == "WikiApi_error message: " +\
        f" {(WIKI_ERROR_RESPONSE.get('errors')[0].get('code'))}"


def test_describe_location_successful_response(mock_wiki_ok_description):
    description = WikiApi.describe_location(9976278)
    assert description == "La place de la République (arabe : ساحة الجمهورية) est une place de Tunis, capitale de la Tunisie."


def test_describe_location_successful_response(mock_wiki_ko_description):
    description = WikiApi.describe_location(9976278)
    assert description == 'No data to be extracted for this place !'
