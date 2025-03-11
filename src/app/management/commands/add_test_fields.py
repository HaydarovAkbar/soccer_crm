import random
from django.core.management.base import BaseCommand
from app.models import Field, FieldOwner
from django.contrib.gis.geos import Point


class Command(BaseCommand):
    help = "Add 20 test fields for Tashkent city"

    def handle(self, *args, **kwargs):
        locations = [
            ("Milliy Stadium", "Tashkent, Yunusabad district", 41.3385, 69.3345),
            ("Pakhtakor Stadium", "Tashkent, Shaykhantohur district", 41.3275, 69.2440),
            ("Bunyodkor Stadium", "Tashkent, Chilanzar district", 41.3021, 69.2320),
            ("Lokomotiv Stadium", "Tashkent, Mirobod district", 41.3156, 69.2563),
            ("Dustlik Stadium", "Tashkent, Mirzo-Ulugbek district", 41.3487, 69.3450),
            ("Alpomish Sport Complex", "Tashkent, Uchtepa district", 41.3104, 69.2773),
            ("Seoul Park Field", "Tashkent, Yakkasaray district", 41.2993, 69.2682),
            ("Greenfield Arena", "Tashkent, Olmazor district", 41.3449, 69.2798),
            ("University Field", "Tashkent, Chilanzar district", 41.3051, 69.2384),
            ("Tashkent Sports Complex", "Tashkent, Sergeli district", 41.2783, 69.1956),
            ("Arena Tashkent", "Tashkent, Mirzo-Ulugbek district", 41.3420, 69.3198),
            ("New Tashkent Stadium", "Tashkent, Yashnabad district", 41.3150, 69.3121),
            ("Mega Sport Field", "Tashkent, Yunusabad district", 41.3333, 69.3333),
            ("Victory Arena", "Tashkent, Shaykhantohur district", 41.3211, 69.2555),
            ("Olympic Stadium", "Tashkent, Chilanzar district", 41.3029, 69.2241),
            ("Uzbekistan Arena", "Tashkent, Uchtepa district", 41.3091, 69.2658),
            ("Central Sport Field", "Tashkent, Yakkasaray district", 41.2960, 69.2783),
            ("Elite Sports Ground", "Tashkent, Olmazor district", 41.3422, 69.2694),
            ("Top Football Field", "Tashkent, Mirzo-Ulugbek district", 41.3501, 69.3410),
            ("UzArena Football Ground", "Tashkent, Sergeli district", 41.2748, 69.2057),
        ]

        for name, address, lat, lon in locations:
            Field.objects.create(
                name=name,
                address=address,
                contact="+998999999999",
                price_per_hour=random.randint(50000, 150000),
                location=Point(lon, lat),
                image="fields/bmc_qr_1.png",
                owner=FieldOwner.objects.first()
            )

        self.stdout.write(self.style.SUCCESS("Successfully added 20 test fields!"))
