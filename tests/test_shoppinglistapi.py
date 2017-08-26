"""
This is a test class
"""
from app import create_app
from base64 import b64encode
from flask import current_app, json, url_for
from models import db, Category, Item, User
import status
from unittest import TestCase

from unittest import TestCase


class InitialTests(TestCase):
    def setUp(self):
        self.app = create_app('test_config')
        self.test_client = self.app.test_client()

        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def get_accept_content_type_headers(self):
        """Helps to add headers on each request"""
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

    def get_authentication_headers(self, username, password):
         """Helps to add authentication  on each request"""
         authentication_headers = self.get_accept_content_type_headers()
        authentication_headers['Authorization'] = \
            'Basic ' + b64encode((username + ':' + password).encode('utf-8')).decode('utf-8')
        return authentication_headers
        

    def test_request_without_authentication(self):
        """
        Ensure we cannot access a resource that requirest authentication without an appropriate authentication header
        """
        pass

    def create_user(self, name, password):
        pass
    def create_category(self, name):
        pass

    def test_create_and_retrieve_category(self):
        """
        Ensure we can create a new Category and then retrieve it
        """
        pass

    def test_create_duplicated_category(self):
        """
        Ensure we cannot create a duplicated Category
        """
        pass

    def test_retrieve_categories_list(self):
        """
        Ensure we can retrieve the categories list
        """
        pass

    def test_update_category(self):
        """
        Ensure we can update the name for an existing category
        """
        pass

    def create_item(self, item, duration, category):
        pass

    def test_create_and_retrieve_item(self):
        """
        Ensure we can create a new item and then retrieve it
        """
        pass

    def test_create_duplicated_item(self):
        """
        Ensure we cannot create a duplicated Item
        """
        pass

    def test_retrieve_items_list(self):
        """
        Ensure we can retrieve the items paginated list
        """
        pass

    def test_update_item(self):
        """
        Ensure we can update a single field for an existing item
        """
        pass
    def test_create_and_retrieve_user(self):
        """
        Ensure we can create a new User and then retrieve it
        """
        pass
