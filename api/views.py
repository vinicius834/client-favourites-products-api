from rest_framework_mongoengine.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, RetrieveAPIView, ListAPIView
from rest_framework_mongoengine.viewsets import GenericViewSet
from rest_framework_mongoengine.contrib.patching import Patch, PatchModelMixin
from mongoengine.errors import  NotUniqueError, ValidationError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from http import HTTPStatus
from rest_framework.permissions import IsAuthenticated
from .serializers import ClientSerializer
from .models import Client
from .product_api import *
from .cache import *
from .constants import *
import json
from django.core import serializers

class ProductDetailView(GenericViewSet, RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_fields = ('product_id')
    def get_product(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        product = ProductApi.product(product_id)
        if product is None:
            return JsonResponse({STATUS: HTTPStatus.NOT_FOUND, ERROR: PRODUCT + ' ' + HTTPStatus.NOT_FOUND.phrase})
        product = json.loads(product.content.decode('utf-8'))
        return JsonResponse({STATUS: HTTPStatus.OK, PRODUCT: product})

class ProductListView(ListAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_fields = ('page_number')
    def get(self, request, *args, **kwargs):
        page_number = kwargs['page_number']
        products = ProductApi.products_by_page_number(page_number)
        if products is None:
            return JsonResponse({STATUS: HTTPStatus.NOT_FOUND, ERROR: HTTPStatus.NOT_FOUND.phrase})
        products = json.loads(products.content.decode('utf-8'))
        return JsonResponse({STATUS: HTTPStatus.OK, PRODUCTS: products})

class ClientCreateListView(ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

    def post(self, request):
        data = request.data
        client_serialized = ClientSerializer(data=data)
        res = None
        if client_serialized.is_valid():
            try:
                client_serialized.save()
            except NotUniqueError:
                return JsonResponse({STATUS: HTTPStatus.BAD_REQUEST, ERROR: DUPLICATED_EMAIL})
        return JsonResponse({STATUS: HTTPStatus.CREATED, CONTENT: client_serialized.data})

class ClientDetailView(GenericViewSet, PatchModelMixin, RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    lookup_fields = ('client_id', 'product_id')

    def put(self, request, *args, **kwargs):
        client_id = kwargs['client_id']
        client = self.search_client(client_id)
        if client is None:
            return JsonResponse({STATUS: HTTPStatus.NOT_FOUND, ERROR: CLIENT + ' ' + HTTPStatus.NOT_FOUND.phrase})
        try:
            client.update(**request.data)
        except NotUniqueError:
            return JsonResponse({STATUS: HTTPStatus.BAD_REQUEST, ERROR: DUPLICATED_EMAIL})
        return JsonResponse({STATUS: HTTPStatus.OK, CONTENT: request.data})

    def get_client(self, request, *args, **kwargs):
        client_id = kwargs['client_id']
        client = self.search_client(client_id)
        if client is None:
            return JsonResponse({STATUS: HTTPStatus.NOT_FOUND, ERROR: CLIENT + ' ' + HTTPStatus.NOT_FOUND.phrase})
        return JsonResponse({STATUS: HTTPStatus.OK, CLIENT: ClientSerializer(client).data})

    def add_favourite_product(self, request, *args, **kwargs):
        client_id = kwargs['client_id']
        client = self.search_client(client_id)
        product_id = request.data['product_id']
        product = ProductApi.product(product_id)
        if not client or not product:
            return JsonResponse({STATUS: HTTPStatus.NOT_FOUND, ERROR: CLIENT + ' or ' + PRODUCT + ' ' + HTTPStatus.NOT_FOUND.phrase})
        try:
            Client.objects(id=client_id).update_one(add_to_set__favourites_products=product_id)
        except Exception:
            return JsonResponse({STATUS: HTTPStatus.BAD_REQUEST})
        return JsonResponse({STATUS: HTTPStatus.OK})

    def remove_favourite_product(self, request, *args, **kwargs):
        product_id = kwargs['product_id']
        client_id = kwargs['client_id']
        client = self.search_client(client_id)
        if client is None:
            return JsonResponse({STATUS: HTTPStatus.NOT_FOUND, ERROR: CLIENT + HTTPStatus.NOT_FOUND.phrase + client_id})
        try:
            Client.objects(id=client_id).update_one(pull__favourites_products=product_id)
        except Exception:
            return JsonResponse({STATUS: HTTPStatus.BAD_REQUEST})
        return JsonResponse({STATUS: HTTPStatus.OK})

    def search_client(self, client_id):
        client = None
        try:
            client = Client.objects.get(id=client_id)
        except (ObjectDoesNotExist, ValidationError):
            client = None
        finally:
            return client






