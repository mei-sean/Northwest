import csv
from reservations.models import Week
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'load weekdays'

    def handle(self, *args, **options):
        days = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        for i,day in enumerate(days):
            Week.objects.create(number=i, name=day)