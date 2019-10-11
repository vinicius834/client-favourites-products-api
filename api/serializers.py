from rest_framework_mongoengine import serializers
from .models import Client

class ClientSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Client
        fields = '__all__'