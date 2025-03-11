from django.utils.dateparse import parse_datetime

from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Field, Booking
from .serializers import FieldSerializer, BookingSerializer, CreateFieldSerializer, CreateBookingSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.gis.geos import Point
from .permissions import FieldOwnerPermission, CustomUserPermission
from .pagination import CustomPagination
from django.utils.timezone import now


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class LoginView(APIView):

    def get(self, request):
        return Response({"message": "Welcome to the football Login API!"}, status=status.HTTP_200_OK)

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogOutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "Welcome to the football Logout API!"}, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class BookFieldView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        field_id = request.data.get("field")
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")

        try:
            field = Field.objects.get(id=field_id)
        except Field.DoesNotExist:
            return Response({"error": "Field not found"}, status=status.HTTP_404_NOT_FOUND)

        if Booking.objects.filter(field=field, start_time=start_time).exists():
            return Response({"error": "This field is already booked for the selected time"},
                            status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.create(
            user=request.user,
            field=field,
            start_time=start_time,
            end_time=end_time
        )

        return Response(
            {"booking_id": booking.id, "message": "Booking confirmed!"},
            status=status.HTTP_201_CREATED
        )


class AvailableFieldsView(ListAPIView):
    serializer_class = FieldSerializer
    filter_backends = [DjangoFilterBackend]
    pagination_class = CustomPagination
    permission_classes = [IsAuthenticated, CustomUserPermission]

    def get_queryset(self):
        queryset = Field.objects.all()

        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")
        if start_date and end_date:
            start_date = parse_datetime(start_date)
            end_date = parse_datetime(end_date)
            booked_fields = Booking.objects.filter(
                start_time__lt=end_date,
                end_time__gt=start_date
            ).values_list("field_id", flat=True)
            queryset = queryset.exclude(id__in=booked_fields)

        longitude = self.request.query_params.get("longitude")
        latitude = self.request.query_params.get("latitude")
        if longitude and latitude:
            try:
                user_location = Point(float(longitude), float(latitude), srid=4326)
                radius_km = 2

                queryset = (
                    queryset.annotate(distance=Distance("location", user_location))
                    .filter(distance__lte=D(km=radius_km))
                    .order_by("distance")
                )

            except (ValueError, TypeError) as e:
                print(f"Error processing location: {e}")

        return queryset


class RetrieveFieldView(RetrieveAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated, CustomUserPermission]
    lookup_field = 'id'
    lookup_url_kwarg = 'field_id'


class CreateBookingView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, CustomUserPermission]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateBookingSerializer
        return BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)



class BookingsView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, FieldOwnerPermission]


class CancelBookingView(DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated, FieldOwnerPermission]
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.end_time() > now().date():
            return Response({"error": "Past bookings cannot be canceled"}, status=status.HTTP_400_BAD_REQUEST)
        booking.delete()
        return Response({"message": "Booking canceled successfully"}, status=status.HTTP_200_OK)


class CreateFieldView(ListCreateAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer
    permission_classes = [IsAuthenticated, FieldOwnerPermission]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateFieldSerializer
        return FieldSerializer
