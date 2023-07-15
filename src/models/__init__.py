from src.extensions import db
from sqlalchemy import PrimaryKeyConstraint


class Topping(db.Model):
    __tablename__ = 'toppings'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return f'<Topping name={self.name}>'


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(75), unique=True)
    toppings = db.relationship("Topping", secondary='pizzatoppings', backref='pizzas')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'toppings': [topping.to_dict() for topping in self.toppings]
        }

    def __repr__(self):
        return f'<Pizza name={self.name}>'


class PizzaToppings(db.Model):
    __tablename__ = 'pizzatoppings'
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'))
    topping_id = db.Column(db.Integer, db.ForeignKey('toppings.id'))
    __table_args__ = (
        PrimaryKeyConstraint('pizza_id', 'topping_id'),
    )

    def to_dict(self):
        return {
            'id': self.id,
            'pizza_id': self.pizza_id,
            'topping_id': self.topping_id
        }

    def __repr__(self):
        return f'<PizzaTopping pizza_id--topping_id == {self.pizza_id}-{self.topping_id}>'
