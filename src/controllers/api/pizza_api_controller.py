from flask import Blueprint

pizza_api = Blueprint("pizza_api",
                      __name__,
                      url_prefix="/api")


@pizza_api.route("/pizzas", methods=["GET"])
def pizza_list():
    return "pizza list"


@pizza_api.route("/pizzas/<int:pizza_id>", methods=["GET"])
def get_pizza_by_id(pizza_id):
    return "pizza by id"


@pizza_api.route("/pizzas", methods=["POST"])
def create_pizza():
    return "create pizza"


@pizza_api.route("/pizzas/<int:pizza_id>", methods=["PUT"])
def update_pizza(pizza_id):
    return "update pizza"


@pizza_api.route("/pizzas/<int:pizza_id>", methods=["DELETE"])
def delete_pizza(pizza_id):
    return "delete pizza"
