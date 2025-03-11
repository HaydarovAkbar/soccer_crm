from django.contrib.auth.models import User
from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D


class FieldOwner(models.Model):
    """The owner of the sports field"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Владелец поля"
        verbose_name_plural = "Владельцы полей"
        db_table = "field_owners"


class GeoManager(models.Manager):
    def nearby(self, latitude, longitude, distance=1000):
        return self.filter(location__distance_lt=(Point(longitude, latitude), D(km=distance)))

    def search(self, query):
        return self.filter(name__icontains=query)


class Field(models.Model):
    """The sports field"""
    owner = models.ForeignKey(FieldOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.TextField()
    contact = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='fields/')
    location = gis_models.PointField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = GeoManager()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Поле"
        verbose_name_plural = "Поля"
        db_table = "fields"


class Booking(models.Model):
    """Booking of a sports field"""
    STATUS = [('pending', 'Pending'),
              ('confirmed', 'Confirmed'),
              ('cancelled', 'Cancelled'),
              ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    field = models.ForeignKey(Field, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=20,
                              choices=STATUS,
                              default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Бронирование"
        verbose_name_plural = "Бронирования"
        db_table = "bookings"

    def __str__(self):
        return f"{self.field.name} - {self.user.username}"
