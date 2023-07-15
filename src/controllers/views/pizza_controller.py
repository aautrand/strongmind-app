import json

from flask import Blueprint, render_template

from src.extensions import db
from src.models import Pizza, Topping
from src.services import PizzaService, ToppingService

pizza_views = Blueprint("pizza_views",
                        __name__,
                        template_folder="templates")

pizza_service = PizzaService(db, Pizza, Topping)
topping_service = ToppingService(db, Topping)


@pizza_views.route("/pizzas", methods=["GET"])
def get_pizza_list():
    pizza_list = json.loads(pizza_service.get_pizzas_list().response[0])["pizzas"]

    for pizza in pizza_list:
        pizza["toppings_string"] = ', '.join([topping['name'] for topping in pizza["toppings"]])

    toppings = json.loads(topping_service.get_toppings_list().response[0])["toppings"]

    return render_template("pizza_list.html", pizza_list=pizza_list, toppings=toppings)


@pizza_views.route("/pizzas/<int:pizza_id>", methods=["GET"])
def get_pizza_by_id(pizza_id):

    pizza = json.loads(pizza_service.get_pizza_by_id(pizza_id).response[0])["pizza"]
    topping_ids = [topping['id'] for topping in pizza['toppings']]
    toppings = json.loads(topping_service.get_toppings_list().response[0])["toppings"]

    return render_template("pizza.html", pizza=pizza, toppings=toppings, topping_ids=topping_ids)
