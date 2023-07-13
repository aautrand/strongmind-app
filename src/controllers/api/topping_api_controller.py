from flask import Blueprint, request

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
    return topping_service.get_topping_by_id(topping_id)


@toppings_api.route("/toppings", methods=["POST"])
def create_topping():
    data = request.get_json()
    topping_name = data["name"]

    return topping_service.create_topping(topping_name)


@toppings_api.route("/toppings/<int:topping_id>", methods=["PUT"])
def update_topping(topping_id):
    data = request.get_json()
    new_topping_name = data["name"]

    return topping_service.update_topping(topping_id=topping_id, new_topping_name=new_topping_name)


@toppings_api.route("/toppings/<int:topping_id>", methods=["DELETE"])
def delete_topping(topping_id):
    return topping_service.delete_topping(topping_id)
