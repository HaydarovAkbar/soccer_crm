from django.contrib import admin
from .models import Field, Booking, FieldOwner

admin.site.register(Field)
admin.site.register(Booking)
admin.site.register(FieldOwner)
