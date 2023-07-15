from flask import Flask
import unittest
from unittest.mock import MagicMock, Mock, call

from src.models import Pizza, Topping
from src.services import PizzaService
from src import db


class TestPizzaService(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()

        self.mock_db = MagicMock()
        self.mock_topping = MagicMock(spec=Topping)
        self.mock_pizza = MagicMock(spec=Pizza)
        self.service = PizzaService(self.mock_db, self.mock_pizza, self.mock_topping)
        self.service = PizzaService(self.mock_db, self.mock_pizza, self.mock_topping)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_pizza_list(self):
        self.mock_pizza.query.all.return_value = [
                Pizza(id=1,
                      name='Basic Pepperoni',
                      toppings=[Topping(id=1, name='pepperoni')])
            ]

        response = self.service.get_pizzas_list()

        # Assertions
        self.mock_pizza.query.all.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"pizzas": [
                {
                    "id": 1,
                    "name": "Basic Pepperoni",
                    "toppings": [
                        {"id": 1, "name": "pepperoni"}
                    ]
                }
            ]
        })

    def test_get_pizza_list_empty(self):
        self.mock_pizza.query.all.return_value = []

        response = self.service.get_pizzas_list()

        # Assertions
        self.mock_pizza.query.all.assert_called_once()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'Pizzas not found'})

    def test_get_pizza_by_id(self):
        self.mock_pizza.query.get.return_value = Pizza(id=1,
                                                       name='Basic Pepperoni',
                                                       toppings=[])

        response = self.service.get_pizza_by_id(1)

        # Assertions
        self.mock_pizza.query.get.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'pizza': {
            "id": 1,
            'name': 'Basic Pepperoni',
            'toppings': []}})

    def test_get_pizza_by_id_missing(self):
        self.mock_pizza.query.get.return_value = None

        response = self.service.get_pizza_by_id(1)

        # Assertions
        self.mock_pizza.query.get.assert_called_once()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'Pizza with id 1 not found'})

    def test_create_pizza(self):
        query_mock = Mock()
        query_mock.first.return_value = None
        self.mock_pizza.query.filter_by.return_value = query_mock

        query_mock2 = Mock()
        query_mock2.first.return_value = Pizza(id=1, name='banana', toppings=[])
        self.mock_pizza.query.filter.return_value = query_mock2

        self.mock_topping.query.filter().count.return_value = 0
        self.mock_topping.query.filter_by().first.return_value = None

        response = self.service.create_pizza("sardines", toppings=[])

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.mock_db.session.add.assert_called_once()
        self.mock_db.session.commit.assert_called_once()

    def test_create_pizza_already_exists(self):
        query_mock = Mock()
        query_mock.first.return_value = Pizza(id=1,
                                              name='banana')
        self.mock_pizza.query.filter.return_value = query_mock

        response = self.service.create_pizza("banana", toppings=[1, 2])

        # Assertions
        self.assertEqual(response.status_code, 409)
        self.mock_pizza.query.filter_by.assert_called_once()

    def test_update_pizza(self):
        query_mock = Mock()
        query_mock.first.return_value = Pizza(id=1, name='banana', toppings=[])

        query_mock2 = Mock()
        query_mock2.first.return_value = None

        self.mock_pizza.query.filter_by.side_effect = [query_mock, query_mock2]

        toppings_mock = Mock()
        toppings_mock.filter.return_value = Mock()
        toppings_mock.filter.return_value.count.return_value = 0  # No existing toppings
        self.mock_topping.query = toppings_mock

        topping_mock = Mock()
        topping_mock.filter_by.return_value = Mock()
        topping_mock.filter_by.return_value.first.return_value = None  # No such topping exists
        Topping.query = topping_mock

        response = self.service.update_pizza(1, 'banana', [])

        # Assertions
        self.assertEqual(response.status_code, 200)

        calls = self.mock_pizza.query.filter_by.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], call(id=1))
        self.assertEqual(calls[1], call(name="banana"))

    def test_update_pizza_missing(self):
        query_mock = Mock()
        query_mock.first.return_value = None
        self.mock_pizza.query.filter_by.return_value = query_mock

        response = self.service.update_pizza(1, "cheese2", [])

        # Assertions
        self.assertEqual(response.status_code, 404)

    def test_update_pizza_duplicate(self):
        query_mock = Mock()
        query_mock.first.return_value = Pizza(id=2, name='avocado')
        self.mock_pizza.query.get.return_value = query_mock

        query_mock2 = Mock()
        query_mock2.first.return_value = Pizza(id=1, name='banana')
        self.mock_pizza.query.filter.return_value = query_mock2

        response = self.service.update_pizza(1, "banana", [])

        # Assertions
        self.assertEqual(response.status_code, 409)

        calls = self.mock_pizza.query.filter_by.call_args_list
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0], call(id=1))
        self.assertEqual(calls[1], call(name="banana"))

    def test_delete_pizza(self):
        query_mock = Mock()
        query_mock.first.return_value = Pizza(id=1, name='banana')
        self.mock_pizza.query.filter_by.return_value = query_mock

        response = self.service.delete_pizza(1)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.mock_db.session.delete.assert_called_once()
        self.mock_db.session.commit.assert_called_once()

    def test_delete_pizza_missing(self):
        query_mock = Mock()
        query_mock.first.return_value = None
        self.mock_pizza.query.filter_by.return_value = query_mock

        response = self.service.delete_pizza(1)

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.mock_pizza.query.filter_by.assert_called_once()


if __name__ == "__main__":
    unittest.main()
