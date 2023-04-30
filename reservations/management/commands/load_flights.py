import random
from datetime import datetime, timedelta
import math


from reservations.models import Airport, Flight, Week
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'load flights'

    def handle(self, *args, **options):
        airports = Airport.objects.all()
        for depart_airport in airports:
            for arrival_airport in airports:
                if depart_airport != arrival_airport: # Ensure we don't create flights from an airport to itself
                    # Create a flight object for this combination of airports
                    now = datetime.now()
                    
                    for days in range(60):
                        current_date = now + timedelta(days=days)
                        start_time = datetime.strptime("09:00", "%H:%M")
                        for time in range(4):
                            a_time = start_time + timedelta(hours=4*time)
                            date_with_time = datetime(now.year, now.month, now.day, a_time.hour, a_time.minute, a_time.second)
                            depart_time = datetime(current_date.year, current_date.month, current_date.day, date_with_time.hour, date_with_time.minute, date_with_time.second)
                            distance = calculate_distance(depart_airport.latitude, depart_airport.longitude, arrival_airport.latitude, arrival_airport.longitude)
                            duration = calculate_duration(distance)
                            arrival_time = depart_time + timedelta(hours=duration['hours'], minutes=duration['minutes'])               
                            flight = Flight(
                                depart_airport=depart_airport,
                                arrival_airport=arrival_airport,
                                depart_time=depart_time,
                                arrival_time=arrival_time,
                                duration = duration,
                                price = 300.00,
                                distance=distance,
                                
                                
                            )
                            flight.save()
                            flight.depart_day.add(Week.objects.get(number=current_date.weekday()))
                        


    
def calculate_distance(lat1, lon1, lat2, lon2):
    # Calculate the distance between two points on Earth using the Haversine formula
    R = 6371  # Radius of the Earth in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = R * c
    return d


def calculate_duration(distance):
    # Calculate the duration of a flight based on the distance and an average speed of 800 km/h
    hours = distance / 800
    minutes = (hours - int(hours)) * 60
    return {'hours': int(hours), 'minutes': int(minutes)}


def generate_random_time():
    # Generate a random datetime object between now and 365 days from now
    now = datetime.now()
    future = now + timedelta(days=45)
    return random.randint(int(now.timestamp()), int(future.timestamp()))


