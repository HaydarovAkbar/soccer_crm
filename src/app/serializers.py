from rest_framework import serializers
from .models import Field, Booking, FieldOwner, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class FieldOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = FieldOwner
        fields = '__all__'


# class FieldSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Field
#         fields = '__all__'


# class BookingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Booking
#         fields = '__all__'


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Field
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    field_name = serializers.CharField(source="field.name", read_only=True)

    class Meta:
        model = Booking
        fields = ["id", "field_name", "date", "start_time", "end_time"]