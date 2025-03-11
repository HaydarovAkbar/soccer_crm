from rest_framework.views import APIView
from rest_framework.generics import ListCreateAPIView, ListAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Field, Booking
from .serializers import FieldSerializer, BookingSerializer
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
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


class BookFieldView(ListCreateAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        field_id = request.data.get("field_id")
        date = request.data.get("date")
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")

        try:
            field = Field.objects.get(id=field_id)
        except Field.DoesNotExist:
            return Response({"error": "Field not found"}, status=status.HTTP_404_NOT_FOUND)

        if Booking.objects.filter(field=field, date=date, start_time=start_time).exists():
            return Response({"error": "This field is already booked for the selected time"},
                            status=status.HTTP_400_BAD_REQUEST)

        booking = Booking.objects.create(
            user=request.user,
            field=field,
            date=date,
            start_time=start_time,
            end_time=end_time
        )

        return Response(
            {"booking_id": booking.id, "message": "Booking confirmed!"},
            status=status.HTTP_201_CREATED
        )


class AvailableFieldsView(ListAPIView):
    queryset = Field.objects.all()
    serializer_class = FieldSerializer

    def get_queryset(self):
        date = self.request.query_params.get("date")
        start_time = self.request.query_params.get("start_time")
        end_time = self.request.query_params.get("end_time")
        return Field.objects.exclude(
            booking__date=date,
            booking__start_time__lt=end_time,
            booking__end_time__gt=start_time
        )


class MyBookingsView(ListAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]


class CancelBookingView(DestroyAPIView):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'booking_id'

    def destroy(self, request, *args, **kwargs):
        booking = self.get_object()
        if booking.date < now().date():
            return Response({"error": "Past bookings cannot be canceled"}, status=status.HTTP_400_BAD_REQUEST)
        booking.delete()
        return Response({"message": "Booking canceled successfully"}, status=status.HTTP_200_OK)
