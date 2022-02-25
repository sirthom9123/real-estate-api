from rest_framework import serializers

from .models import Listings


class ListingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Listings
        fields = '__all__'