from flask import Blueprint, render_template, send_file, url_for
from monolith import db
from monolith.models import Restaurant
import folium

restaurants_map = Blueprint("restaurants_map", __name__)


@restaurants_map.route("/restaurants_map")
def show_map():
    restaurants = db.session.query(
        Restaurant.name, Restaurant.phone, Restaurant.lat, Restaurant.lon, Restaurant.id
    ).all()
    # let's make a map and populate it out of every restaurants we have
    m = folium.Map(location=[restaurants[0].lat, restaurants[0].lon])
    for restaurant in restaurants:
        link = '<a href= "' + url_for("restaurants.restaurant_sheet", restaurant_id=restaurant.id) + \
            '" target="_blank"> Restaurant Details </a>'
        folium.Marker(
            (restaurant.lat, restaurant.lon),
            popup=link,
            tooltip=restaurant.name,
        ).add_to(m)

    m.save("./monolith/templates/map.html")
    return render_template("map_page.html")


@restaurants_map.route("/map.html")
def send_map():
    return send_file("./templates/map.html")
