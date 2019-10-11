from django.contrib import admin
from django.urls import path
from .views import *

# client_list_action = {
#     'get': 'list',
#     'post': 'create'
# }
#
# client_actions = {
#     'get': 'get_client',
#     ' put': 'put',
#     'patch': 'add_favourite_product',
#     'delete': 'remove_favourite_product'
# }

urlpatterns = [
    path('client/', ClientCreateListView.as_view()),
    path('client/<str:client_id>', ClientDetailView.as_view({'get': 'get_client', ' put': 'put'})),
    path('client/<str:client_id>/favourite_product/', ClientDetailView.as_view({'patch': 'add_favourite_product'})),
    path('client/<str:client_id>/favourite_product/<str:product_id>', ClientDetailView.as_view({'delete': 'remove_favourite_product'})),
    path('product/<int:page_number>', ProductListView.as_view()),
    path('product/<str:product_id>', ProductDetailView.as_view({'get': 'get_product'}))
]
