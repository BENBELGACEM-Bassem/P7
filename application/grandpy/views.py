"""Main module for Granpy website"""

from flask import render_template, url_for, request, jsonify

from .app import app

from .utils.main import get_data_for

@app.route("/", methods=['GET'])
@app.route("/home", methods=['GET'])
def home():
    """Initiate the home/main page"""
    return render_template("index.html")


@app.route('/ajax', methods=['POST'])
def treat_request():
    """
    Store user request, parse it to extract a place name, 
    get adress and coordinates from GoogleMaps for this place
    and call MediaWiki API to extract its description.
    """

    user_request = request.form["user_input"]
    response = get_data_for(user_request)
    return jsonify(response)


