from rest_framework.test import APIRequestFactory, APITestCase, APIClient
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from http import HTTPStatus
from .models import Client
import json
from mongoengine.connection import _get_db
#import pymongo

class BaseTest(APITestCase):
    def mongo_conn(self):
        pass

    def close(self):
        _get_db()['test']['test'].drop()

class ClientCreateListView(BaseTest):

    def setUp(self):
        self.db = _get_db()
        self.user = User.objects.create_user(username='test')
        token = Token.objects.create(key='test_token', user=self.user)
        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        try:
            self.client = Client.objects.get(email='test@test.com')
        except Exception:
            self.client = Client.objects.create(name='test', email='test@test.com')

    def tearDown(self):
        self.close()

    def test_post(self):
        self.db['client'].drop()
        data =  { "name": "fulano", "email": "fulano@gmail.com", 'favourites_products': [] }
        response = self.api_client.post('/client/', data, format='json')
        client = json.loads(response.content.decode('utf-8'))
        self.assertEqual(client['status'], HTTPStatus.CREATED)
        self.assertEqual(client['content']['name'], data['name'])

    def test_list_clients(self):
        response = self.api_client.get('/client/')
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(len(response.data) > 0)

    def test_put(self):
        _get_db()['test']['client'].drop()
        response = self.api_client.put('/client/' + str(self.client.id), {'name':'test_put'}, format='json')
        client_after = Client.objects.get(id=self.client.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertFalse(self.client.name == client_after.name)

    def test_get(self):
        response = self.api_client.get('/client/' + str(self.client.id))
        client = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(self.client.name, client['client']['name'])

    def test_add_favourite_product(self):
        product_id = '958ec015-cfcf-258d-c6df-1721de0ab6ea'
        url = '/client/' + str(self.client.id) + '/favourite_product/'
        response = self.api_client.patch(url, {'product_id': product_id}, format='json')
        client_after = Client.objects.get(id=self.client.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(len(client_after.favourites_products) > 0)
        self.assertTrue(product_id, client_after.favourites_products[0])

    def test_remove_add_favourite_product(self):
        product_id = '958ec015-cfcf-258d-c6df-1721de0ab6ea'
        url = '/client/' + str(self.client.id) + '/favourite_product/' + product_id
        response = self.api_client.delete(url)
        client_after = Client.objects.get(id=self.client.id)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(len(client_after.favourites_products) == 0)

class ProductDetailView(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        token = Token.objects.create(key='test_token', user=self.user)
        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_get_product(self):
        product_id = '958ec015-cfcf-258d-c6df-1721de0ab6ea'
        url = '/product/' + product_id
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_get_product(self):
        product_id = '958ec015-cfcf-258d-c6df-1721de0ab6ea'
        url = '/product/' + product_id
        response = self.api_client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

class ProductListView(BaseTest):
    def setUp(self):
        self.user = User.objects.create_user(username='test')
        token = Token.objects.create(key='test_token', user=self.user)
        self.api_client = APIClient()
        self.api_client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        try:
            self.client = Client.objects.get(email='test1@test.com')
        except Exception:
            self.client = Client.objects.create(name='test', email='test1@test.com')



    def test_list_products_by_page(self):
        response = self.api_client.get('/product/1')
        products = json.loads(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, HTTPStatus.OK)