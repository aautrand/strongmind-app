from flask import jsonify
from src.models import Topping
from src.decorators import common_response


class ToppingService:

    def __init__(self, db, topping):
        self.db = db
        self.topping = topping

    @common_response
    def get_toppings_list(self):
        toppings_list = self.topping.query.all()

        if not toppings_list:
            return jsonify(message='Toppings not found'), 404

        toppings_json = [topping.to_dict() for topping in toppings_list]
        return jsonify(toppings=toppings_json)

    @common_response
    def get_topping_by_id(self, topping_id):

        topping = self.topping.query.get(topping_id)

        if not topping:
            return jsonify(message=f'Topping with id {topping_id} not found'), 404

        return jsonify(topping=topping.to_dict())

    @common_response
    def create_topping(self, topping_name):

        conflicting_topping = self.topping.query.filter(Topping.name == topping_name).first()

        if conflicting_topping:
            return jsonify(message=f"Topping with name {topping_name} already exists"), 409

        new_topping = Topping(name=topping_name)

        self.db.session.add(new_topping)
        self.db.session.commit()

        return jsonify(topping=new_topping.to_dict())

    @common_response
    def update_topping(self, topping_id, new_topping_name):

        old_topping = self.topping.query.get(topping_id).first()

        if not old_topping:
            return jsonify(message=f'Topping with id {topping_id} not found'), 404

        conflicting_topping = self.topping.query.filter(Topping.name == new_topping_name).first()
        if conflicting_topping:
            return jsonify(message=f"Topping with name {new_topping_name} already exists"), 409

        old_topping.name = new_topping_name

        self.db.session.commit()

        return jsonify(topping=old_topping.to_dict())

    @common_response
    def delete_topping(self, topping_id):

        topping = self.topping.query.get(topping_id)

        if not topping:
            return jsonify(message=f'Topping with id {topping_id} not found'), 404

        self.db.session.delete(topping)
        self.db.session.commit()

        return jsonify(message="Topping successfully deleted")
