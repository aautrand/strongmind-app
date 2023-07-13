from flask import jsonify
from src.models import Topping
from src.decorators import common_response


class ToppingService:

    def __init__(self, db):
        self.db = db
        self.topping = Topping

    @common_response
    def get_toppings_list(self):
        toppings_list = self.topping.query.all()

        if not toppings_list:
            return jsonify(message='Toppings not found'), 404

        toppings_json = [topping.to_dict() for topping in self.topping.query.all()]
        return jsonify(toppings=toppings_json)

    def get_topping_by_id(self, topping_id):
        topping = self.topping.query.get(topping_id)

        if not topping:
            return jsonify(message=f'Topping with id {topping_id} not found'), 404

        return jsonify(toppings=topping.to_dict())

    def create_topping(self):
        pass

    def update_topping(self, topping_id):
        pass

    def delete_topping(self, topping_id):
        pass
