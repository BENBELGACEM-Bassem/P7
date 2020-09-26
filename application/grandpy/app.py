#! /usr/bin/env python3
# coding: utf-8

"""Module to create an application with flask"""

from flask import Flask

app = Flask(__name__)

from . import views
