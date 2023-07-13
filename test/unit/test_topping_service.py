from flask import Flask
import unittest
from unittest.mock import MagicMock

from src.models import Topping
from src.services import ToppingService
from src import db


class TestToppingService(unittest.TestCase):

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
        self.service = ToppingService(self.mock_db, self.mock_topping)

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()

    def test_get_topping_list(self):
        self.mock_topping.query.all.return_value = [
            Topping(id=1, name='Topping 1'),
            Topping(id=2, name='Topping 2'),
            Topping(id=3, name='Topping 3')
        ]

        response = self.service.get_toppings_list()

        # Assertions
        self.mock_topping.query.all.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'toppings': [
            {"id": 1, 'name': 'Topping 1'},
            {"id": 2, 'name': 'Topping 2'},
            {"id": 3, 'name': 'Topping 3'}]})

    def test_get_topping_list_empty(self):
        self.mock_topping.query.all.return_value = [
        ]

        response = self.service.get_toppings_list()

        # Assertions
        self.mock_topping.query.all.assert_called_once()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'Toppings not found'})


if __name__ == "__main__":
    unittest.main()
