from rest_framework import serializers

from prototype.models import PrototypeModel


class PrototypeSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'
        model = PrototypeModel

