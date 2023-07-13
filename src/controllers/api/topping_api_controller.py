from flask import Blueprint

from src.extensions import db
from src.services import ToppingService

toppings_api = Blueprint("toppings_api",
                         __name__,
                         url_prefix="/api")

topping_service = ToppingService(db)


@toppings_api.route("/toppings", methods=["GET"])
def toppings_list():
    return topping_service.get_toppings_list()


@toppings_api.route("/toppings/<int:topping_id>", methods=["GET"])
def get_topping_by_id(topping_id):
    return "topping by id"


@toppings_api.route("/toppings", methods=["POST"])
def create_topping():
    return "create topping"


@toppings_api.route("/toppings/<int:topping_id>", methods=["PUT"])
def update_topping(topping_id):
    return "update topping"


@toppings_api.route("/toppings/<int:topping_id>", methods=["DELETE"])
def delete_topping(topping_id):
    return "delete topping"
