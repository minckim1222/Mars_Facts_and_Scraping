#import libraries
from flask import Flask, render_template, redirect
import pymongo

#create flask app
app = Flask(__name__)

#create pymongo client
client = pymongo.Mongoclient()
db = client.mars_db
