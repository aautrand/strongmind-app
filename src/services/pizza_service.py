from flask import jsonify
from src.models import Pizza, Topping
from src.decorators import common_response


class PizzaService:

    def __init__(self, db, pizza, toppings):
        self.db = db
        self.pizza = pizza
        self.toppings = toppings

    @common_response
    def get_pizzas_list(self):
        pizzas_list = self.pizza.query.all()

        if not pizzas_list:
            return jsonify(message='Pizzas not found'), 404

        pizzas_json = [pizza.to_dict() for pizza in pizzas_list]
        return jsonify(pizzas=pizzas_json)

    @common_response
    def get_pizza_by_id(self, pizza_id):

        pizza = self.pizza.query.get(pizza_id)

        if not pizza:
            return jsonify(message=f'Pizza with id {pizza_id} not found'), 404

        return jsonify(pizza=pizza.to_dict())

    @common_response
    def create_pizza(self, pizza_name, toppings):

        conflicting_pizza = self.pizza.query.filter_by(name=pizza_name).first()

        if conflicting_pizza:
            return jsonify(message=f"Pizza with name {pizza_name} already exists"), 409

        new_pizza = Pizza(name=pizza_name)
        new_pizza.toppings = []

        if toppings:
            existing_toppings_count = self.toppings.query \
                .filter(Topping.id.in_(toppings)) \
                .count()

            if existing_toppings_count != len(toppings):
                return jsonify(message=f"Some of the ingredients in this pizza are missing"), 400

            for topping_id in toppings:
                topping = Topping.query.filter_by(id=topping_id).first()
                if topping:
                    new_pizza.toppings.append(topping)
                else:
                    return jsonify(message=f"Some of the ingredients in this pizza are missing"), 400

        self.db.session.add(new_pizza)
        self.db.session.commit()

        return jsonify(pizza=new_pizza.to_dict())

    @common_response
    def update_pizza(self, pizza_id, new_pizza_name, new_toppings):

        old_pizza = self.pizza.query.filter_by(id=pizza_id).first()

        if not old_pizza:
            return jsonify(message=f"Pizza with id {pizza_id} does not exists"), 404

        conflicting_pizza = self.pizza.query.filter_by(name=new_pizza_name).first()

        if conflicting_pizza:
            return jsonify(message=f"Pizza with name {new_pizza_name} already exists"), 409

        old_pizza.name = new_pizza_name

        if new_toppings:
            existing_toppings_count = self.toppings.query \
                .filter(Topping.id.in_(new_toppings)) \
                .count()

            if existing_toppings_count != len(new_toppings):
                return jsonify(message=f"Some of the ingredients in this pizza are missing"), 400

            for topping_id in new_toppings:
                topping = Topping.query.filter_by(id=topping_id).first()
                if topping:
                    old_pizza.toppings.append(topping)
                else:
                    return jsonify(message=f"Some of the ingredients in this pizza are missing"), 400

        self.db.session.commit()

        return jsonify(pizza=old_pizza.to_dict())

    @common_response
    def delete_pizza(self, pizza_id):

        pizza = self.pizza.query.filter_by(id=pizza_id).first()

        if not pizza:
            return jsonify(message=f'Pizza with id {pizza_id} not found'), 404

        self.db.session.delete(pizza)
        self.db.session.commit()

        return jsonify(message="Pizza successfully deleted")
