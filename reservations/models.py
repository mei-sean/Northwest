from django.db import models
from django.conf import settings
from geopy.distance import geodesic
import datetime


class Airport(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Week(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.name} ({self.number})"
    
class Flight(models.Model):
    depart_airport = models.ForeignKey(Airport, related_name='depart_flights', on_delete=models.CASCADE)
    arrival_airport = models.ForeignKey(Airport, related_name='arrival_flights', on_delete=models.CASCADE)
    depart_time = models.DateTimeField(default=datetime.timedelta(0))
    arrival_time = models.DateTimeField(default=datetime.timedelta(0))
    duration = models.DurationField()
    distance = models.FloatField()
    price = models.FloatField()
    seats = models.PositiveIntegerField(default=0)
    economy_fare = models.FloatField(null=True)
    business_fare = models.FloatField(null=True)
    first_fare = models.FloatField(null=True)
    depart_day = models.ManyToManyField(Week, related_name="flights_of_the_day")

    def __str__(self):
        return f"{self.depart_airport} to {self.arrival_airport} ({self.depart_time.strftime('%Y-%m-%d %H:%M')})"

    def save(self, *args, **kwargs):
        self.distance = geodesic((self.depart_airport.latitude, self.depart_airport.longitude),
                                  (self.arrival_airport.latitude, self.arrival_airport.longitude)).miles
        self.duration = self.arrival_time - self.depart_time
        super(Flight, self).save(*args, **kwargs)

    def check_seats(self):
        return self.seats < 250
    
class AccountInfo(models.Model):
    userID = models.PositiveIntegerField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.CharField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.IntegerField(max_length=16)
    country = models.CharField(max_length=100)
    
    def save(self, request=None, *args, **kwargs):
        self.userID = request.user.id
        super(AccountInfo, self).save(*args, **kwargs)








