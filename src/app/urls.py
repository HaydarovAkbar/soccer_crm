from django.urls import path
from .views import FieldListView, CustomAuthToken, ObtainAuthToken

urlpatterns = [
    path('fields/', FieldListView.as_view(), name='field-list'),
    path('auth/', CustomAuthToken.as_view(), name='auth'),
    path('login/', ObtainAuthToken.as_view(), name='login'),
]
