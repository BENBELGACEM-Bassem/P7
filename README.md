README P7:

# Scope

This is the 7th project developed for Openclassrooms. It delivers a web application to interact with a user looking for a place.
The GrandPy robot, as is the name of this application, will provide you with an adress, a map view and some pieces of information about the wanted location

#Specificities

You have to possess a Google Cloud API Key in order to get this program running. 
You have to activate Geocoding API and Maps Javascript API

# Setting up

Once you clone this repository and in order to run it, you need to
prepare your virtual environment by first creating it, for example using pipenv:
pip3 install pipenv
pipenv install

Then install the dependencies with pip install requirements.txt
Insert your API key in the config.py file, by replacing GMGEO_KEY and GMAPS_KEY variables, 
(use environment variables to protect your credentials)

# Launching

Go the the project's root on your terminal and launch: python run.py
Launch you web browser and go to the local server, localhost:5000 by default
Write your question in the form and tap enter, wait for GrandPy to answer you.

# Testing

Pytest is the library being used in this program. In order to run the tests, do like so :
Go the the project's root on your terminal
Run pytest (Pytest has to be installed)
If the test is validated, it will be green

# Heroku

Visit this link,please: https://bbbgrandpy.herokuapp.com/

