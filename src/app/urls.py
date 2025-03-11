from django.urls import path
from .views import LoginView, BookFieldView, AvailableFieldsView, MyBookingsView, CancelBookingView , LogOutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogOutView.as_view(), name='logout'),
    path('book-field/', BookFieldView.as_view(), name='book-field'),
    path('available-fields/', AvailableFieldsView.as_view(), name='available-fields'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
    path('cancel-booking/<int:booking_id>/', CancelBookingView.as_view(), name='cancel-booking')
]
