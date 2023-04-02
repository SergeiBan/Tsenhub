from rest_framework import serializers
from parts.models import Part


class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part
        fields = ('name', 'uid', 'initial_price')


class PriceListSerializer(serializers.Serializer):

    pricelist = serializers.FileField()
