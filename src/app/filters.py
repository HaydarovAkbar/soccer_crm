import django_filters
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from datetime import datetime
from .models import Field


class FieldFilter(django_filters.FilterSet):
    start_date = django_filters.IsoDateTimeFilter(method="filter_available_fields", field_name="start_date")
    end_date = django_filters.IsoDateTimeFilter(method="filter_available_fields", field_name="end_date")
    longitude = django_filters.NumberFilter(method="filter_nearby_fields", field_name="location")
    latitude = django_filters.NumberFilter(method="filter_nearby_fields", field_name="location")

    class Meta:
        model = Field
        fields = ["start_date", "end_date", "longitude", "latitude"]

    def filter_available_fields(self, queryset, name, value):
        start_time = self.data.get("start_date")
        end_time = self.data.get("end_date")

        if start_time and end_time:
            try:
                start_time = datetime.fromisoformat(start_time)
                end_time = datetime.fromisoformat(end_time)
            except ValueError:
                return queryset.none()

            booked_fields = Field.objects.filter(
                booking__start_time__lt=end_time,
                booking__end_time__gt=start_time
            ).values_list("id", flat=True)

            return queryset.exclude(id__in=booked_fields)

        return queryset

    def filter_nearby_fields(self, queryset, name, value):
        longitude = self.data.get("longitude")
        latitude = self.data.get("latitude")
        radius = self.data.get("radius", 10)

        if longitude and latitude:
            try:
                longitude = float(longitude)
                latitude = float(latitude)
                radius = float(radius)
            except ValueError:
                return queryset.none()

            user_location = Point(longitude, latitude, srid=4326)
            return queryset.annotate(distance=Distance("location", user_location)).filter(
                location__distance_lte=(user_location, D(km=radius))
            ).order_by("distance")

        return queryset
