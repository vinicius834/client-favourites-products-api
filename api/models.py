from django.db import models
from mongoengine import Document, EmbeddedDocument, fields

class Client(Document):
    name = fields.StringField(min_length=3, max_length=100, required=True)
    email = fields.EmailField(required=True, unique=False)
    favourites_products = fields.ListField()
