from rest_framework.views import APIView
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
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({"token": tokens["access"]}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class BookFieldView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        field_id = request.data.get("field_id")
        date = request.data.get("date")
        start_time = request.data.get("start_time")
        end_time = request.data.get("end_time")

        try:
            field = Field.objects.get(id=field_id)
        except Field.DoesNotExist:
            return Response({"error": "Field not found"}, status=status.HTTP_404_NOT_FOUND)

        if Booking.objects.filter(field=field, date=date, start_time=start_time).exists():
            return Response({"error": "This field is already booked for the selected time"}, status=status.HTTP_400_BAD_REQUEST)

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


class AvailableFieldsView(APIView):
    def get(self, request):
        fields = Field.objects.all()
        serializer = FieldSerializer(fields, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MyBookingsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CancelBookingView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, booking_id):
        try:
            booking = Booking.objects.get(id=booking_id, user=request.user)

            if booking.date < now().date():
                return Response({"error": "Past bookings cannot be canceled"}, status=status.HTTP_400_BAD_REQUEST)

            booking.delete()
            return Response({"message": "Booking canceled successfully"}, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            return Response({"error": "Booking not found"}, status=status.HTTP_404_NOT_FOUND)