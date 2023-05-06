import csv
from reservations.models import Airport
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Loads the top 50 US airports into the database'

    def handle(self, *args, **options):
        with open('airports.csv') as f:
            reader = csv.reader(f)
            next(reader)  # skip header row
            for row in reader:
                code, name, city, state, latitude, longitude = row
                Airport.objects.create(code=code, name=name, city=city, state=state, latitude=latitude, longitude=longitude)