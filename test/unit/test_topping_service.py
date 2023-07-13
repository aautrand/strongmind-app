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

    def test_get_toppings_list(self):
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

    def test_get_toppings_list_empty(self):
        self.mock_topping.query.all.return_value = [
        ]

        response = self.service.get_toppings_list()

        # Assertions
        self.mock_topping.query.all.assert_called_once()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'Toppings not found'})

    def test_get_topping_by_id(self):
        self.mock_topping.query.get.return_value = Topping(id=1, name="Topping 1")

        response = self.service.get_topping_by_id(1)

        # Assertions
        self.mock_topping.query.get.assert_called_once()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {'topping': {"id": 1, 'name': 'Topping 1'}})

    def test_get_topping_by_id_missing(self):
        self.mock_topping.query.get.return_value = None

        response = self.service.get_topping_by_id(1)

        # Assertions
        self.mock_topping.query.get.assert_called_once()
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {'message': 'Topping with id 1 not found'})

    def test_create_topping(self):
        self.mock_topping.query.filter.return_value = None

        response = self.service.create_topping("sardines")

        # Assertions
        self.mock_db.session.add.assert_called_once()
        self.assertEqual(response.status_code, 200)

    def test_update_topping(self):
        self.mock_topping.query.get.return_value = Topping(id=1, name='cheese')
        self.mock_topping.query.filter.return_value = None

        response = self.service.update_topping(1, "cheese2")

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.mock_topping.query.get.assert_called_once()
        self.mock_topping.query.filter.assert_called_once()
        self.mock_db.session.commit.assert_called_once()

    def test_update_topping_missing(self):
        self.mock_topping.query.get.return_value = None

        response = self.service.update_topping(1, "cheese2")

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.mock_topping.query.get.assert_called_once()

    def test_update_topping_duplicate(self):
        self.mock_topping.query.get.return_value = Topping(id=1, name='cheese')
        self.mock_topping.query.filter.return_value = Topping(id=2, name='cheese2')

        response = self.service.update_topping(1, "cheese2")

        # Assertions
        self.assertEqual(response.status_code, 409)
        self.mock_topping.query.get.assert_called_once()
        self.mock_topping.query.filter.assert_called_once()

    def test_delete_topping(self):
        self.mock_topping.query.get.return_value = Topping(id=1, name='cheese')

        response = self.service.delete_topping(1)

        # Assertions
        self.assertEqual(response.status_code, 200)
        self.mock_topping.query.get.assert_called_once()
        self.mock_db.session.delete.assert_called_once()
        self.mock_db.session.commit.assert_called_once()

    def test_delete_topping_missing(self):
        self.mock_topping.query.get.return_value = None

        response = self.service.delete_topping(1)

        # Assertions
        self.assertEqual(response.status_code, 404)
        self.mock_topping.query.get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
