from flask import Blueprint, render_template

from monolith import db
from monolith.models import Restaurant

import os

home = Blueprint("home", __name__)


@home.route("/")
def index():
    restaurants = [res.__dict__ for res in db.session.query(Restaurant).all()]
    images_path_dict = {}
    for el in restaurants:
        # print(el)
        path = "./monolith/static/uploads/" + str(el["id"])
        photos_paths = os.listdir(path)
        # gets only the first one
        if photos_paths:
            el["path"] = os.path.basename(photos_paths[0])

    return render_template(
        "index.html", restaurants=restaurants, paths=images_path_dict
    )
