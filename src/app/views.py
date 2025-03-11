from django.http import JsonResponse
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Field, Booking, FieldOwner, User
from .serializers import FieldSerializer, BookingSerializer, FieldOwnerSerializer, UserSerializer


class FieldListView(ListAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer