from src.models import Topping


class ToppingService:

    def __init__(self, db):
        self.db = db
        self.topping = Topping

    def get_toppings_list(self):
        return {"toppings": [topping.to_dict() for topping in self.topping.query.all()]}

    def get_topping_by_id(self, topping_id):
        pass

    def create_topping(self):
        pass

    def update_topping(self, topping_id):
        pass

    def delete_topping(self, topping_id):
        pass
