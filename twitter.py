import urllib.request
import urllib.parse
import urllib.error
import json
import folium
from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter
import ssl
import sys
import twurl
from flask import Flask, redirect, url_for, render_template, request

# https://apps.twitter.com/
# Create App and get the four strings, put them in hidden.py

TWITTER_URL = 'https://api.twitter.com/1.1/friends/list.json'

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

app = Flask(__name__)

def make_info(acct):
    if len(acct) < 1:
        sys.exit()
    url = twurl.augment(TWITTER_URL,
                        {'screen_name': acct, 'count': '10'})
    connection = urllib.request.urlopen(url, context=ctx)
    data = connection.read().decode()
    js = json.loads(data)
    data = js['users']
    users = {}
    for iiter in data:
        users[iiter['screen_name']] = iiter['location']
    return users


def make_coordinates(users):
    geolocator = Nominatim(user_agent='locations')
    locationsdct = {}
    for key, value in users.items():
        location = geolocator.geocode(value)
        if location is not None:
            locationsdct[key] = [location.latitude, location.longitude]
    return locationsdct

def make_map(locationsdct):
    """
    Makes a map out od data, stated in previous functions.
    """
    map = folium.Map(zoom_start=4, tiles="Stamen Terrain", control_scale=True)
    locs_markers = folium.FeatureGroup(name = 'locations')
    map.add_child(locs_markers)
    for key, value in locationsdct.items():
        locs_markers.add_child(folium.Marker(location = value, popup = key))
    map.add_child(folium.LayerControl())
    return map._repr_html_()

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        username = request.form['screen_name']
        return redirect(url_for("user", usr= username))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user(usr):
    return make_map(make_coordinates(make_info(usr)))



if __name__ =="__main__":
    app.run(debug=True)
