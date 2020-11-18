from flask import Blueprint, render_template
from monolith import db
from monolith.models import Restaurant

restaurants_map = Blueprint("restaurants_map", __name__)


@restaurants_map.route("/restaurants/map")
def show_map():
    restaurants = db.session.query(
        Restaurant.name, Restaurant.phone, Restaurant.lat, Restaurant.lon, Restaurant.id
    ).all()
    return render_template("map_page.html", restaurant_list=restaurants)
