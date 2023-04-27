from rest_framework import serializers

from parts.models import Part


class PartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Part
        fields = ('uid', 'initial_price')


class PriceListSerializer(serializers.Serializer):

    quotes_request = serializers.FileField()
