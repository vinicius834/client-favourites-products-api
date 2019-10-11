from django.urls import path
from .views import *


urlpatterns = [
    path('client/', ClientCreateListView.as_view()),
    path('client/<str:client_id>', ClientDetailView.as_view({'get': 'get_client', ' put': 'put', 'delete': 'delete'})),
    path('client/<str:client_id>/favourite_product/', ClientDetailView.as_view({'patch': 'add_favourite_product'})),
    path('client/<str:client_id>/favourite_product/<str:product_id>', ClientDetailView.as_view({'delete': 'remove_favourite_product'})),
    path('product/<int:page_number>', ProductListView.as_view()),
    path('product/<str:product_id>', ProductDetailView.as_view({'get': 'get_product'}))
]
