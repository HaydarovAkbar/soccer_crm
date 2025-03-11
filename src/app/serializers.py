from rest_framework import serializers
from .models import Field, Booking, FieldOwner, User
from django.contrib.gis.geos import Point


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FieldOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOwner
        fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    # field_name = serializers.CharField(source="field.name", read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "field", "start_time", "end_time"]


class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ["field", "start_time", "end_time"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class CreateFieldSerializer(serializers.ModelSerializer):
    longitude = serializers.FloatField(write_only=True)
    latitude = serializers.FloatField(write_only=True)

    class Meta:
        model = Field
        fields = ("name", "address", "contact", "price_per_hour", "image", "longitude", "latitude")

    def create(self, validated_data):
        longitude = validated_data.pop("longitude")
        latitude = validated_data.pop("latitude")
        location = Point(longitude, latitude)
        validated_data["location"] = location
        validated_data["owner"] = self.context["request"].user
        return super().create(validated_data)
