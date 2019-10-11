from django.http import JsonResponse
from http import HTTPStatus
from .cache import *
from .constants import *
import requests
import json

class ProductApi:
    @classmethod
    def products_by_page_number(cls, page_number=None):
        products = None
        url = 'http://challenge-api.luizalabs.com/api/product/?page='
        if not page_number:
            page_number = 1
            products = Cache.get(1)
        else:
            products = Cache.get(page_number)
        if not products:
            url = url + str(int(page_number))
            response = requests.get(url)
            if response.status_code == HTTPStatus.NOT_FOUND:
                return None
            else:
                products = response.json()
                Cache.save(page_number, str(products))
        return JsonResponse({PRODUCTS: str(products)})

    @classmethod
    def product(cls, product_id=None):
        if product_id == None:
            raise ValueError('Id is invalid.')
        response = cls.check_product_cache(product_id)
        return response

    @classmethod
    def check_product_cache(cls, product_id):
        response = None
        product = Cache.get(product_id)
        if product:
            return JsonResponse({PRODUCT: str(product.decode('utf-8'))})
        response = cls.product_by_id(product_id)
        if not response:
            return None
        Cache.save(product_id, str(response.json()))
        return JsonResponse({PRODUCT: str(response.json())})

    @classmethod
    def product_by_id(cls, product_id):
        response = requests.get('http://challenge-api.luizalabs.com/api/product/{id}'.format(id=product_id))
        if response.status_code == HTTPStatus.NOT_FOUND:
            return None
        return response