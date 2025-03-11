from .views import FieldListView
from django.urls import path

urlpatterns = [
    path('fields/', FieldListView.as_view(), name='field-list'),
]