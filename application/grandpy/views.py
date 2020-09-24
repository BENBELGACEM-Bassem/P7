"""Main module for Granpy website"""

import os

from flask import render_template, url_for, request, jsonify

from .app import app

from .utils.main import get_data_for

from .utils.config import GmapsParams

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    """Initiate the home/main page"""
    return render_template("index.html", key=GmapsParams.GMAPS_KEY)


@app.route('/ajax', methods=['POST'])
def treat_request():
    """
    Store user request, parse it to extract a place name,
    get adress and coordinates from GoogleMaps for this place
    and call MediaWiki API to extract its description.
    """

    # Retrieve request from the browser
    user_request = request.form["question"]
    # Process the query on the backend side
    response = get_data_for(user_request)
    # Return json data format to the browser
    return jsonify(response)
