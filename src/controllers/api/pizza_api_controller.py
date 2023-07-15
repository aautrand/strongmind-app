from flask import Blueprint, request

from src.extensions import db
from src.models import Pizza, Topping
from src.services import PizzaService

pizza_api = Blueprint("pizza_api",
                      __name__,
                      url_prefix="/api")

pizza_service = PizzaService(db, Pizza, Topping)


@pizza_api.route("/pizzas", methods=["GET"])
def pizza_list():
    return pizza_service.get_pizzas_list()


@pizza_api.route("/pizzas/<int:pizza_id>", methods=["GET"])
def get_pizza_by_id(pizza_id):
    return pizza_service.get_pizza_by_id(pizza_id)


@pizza_api.route("/pizzas", methods=["POST"])
def create_pizza():
    data = request.get_json()
    pizza = data["name"]
    toppings = data["toppings"]

    return pizza_service.create_pizza(pizza, toppings)


@pizza_api.route("/pizzas/<int:pizza_id>", methods=["PUT"])
def update_pizza(pizza_id):
    data = request.get_json()
    pizza_name = data["name"]
    toppings = data["toppings"]

    return pizza_service.update_pizza(pizza_id, pizza_name, toppings)


@pizza_api.route("/pizzas/<int:pizza_id>", methods=["DELETE"])
def delete_pizza(pizza_id):
    return pizza_service.delete_pizza(pizza_id)
