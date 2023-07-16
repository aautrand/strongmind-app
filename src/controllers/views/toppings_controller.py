import json

from flask import Blueprint, render_template

from src.extensions import db
from src.models import Topping
from src.services import ToppingService

topping_views = Blueprint("topping_views",
                          __name__,
                          template_folder="templates")

topping_service = ToppingService(db, Topping)


@topping_views.route("/toppings", methods=["GET"])
def get_toppings_list():
    toppings = json.loads(topping_service.get_toppings_list().response[0])["toppings"]

    return render_template("toppings_list.html", toppings=toppings)


@topping_views.route("/toppings/<int:topping_id>", methods=["GET"])
def get_topping_by_id(topping_id):
    topping = json.loads(topping_service.get_topping_by_id(topping_id).response[0])["topping"]

    return render_template("topping.html", topping=topping)
