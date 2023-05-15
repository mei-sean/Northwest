from django.db import models
from django.conf import settings
from geopy.distance import geodesic
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


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
    depart_time = models.DateTimeField(default=timedelta(0))
    arrival_time = models.DateTimeField(default=timedelta(0))
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
        return self.seats < 500
    
class Passenger(models.Model):
    first_name =  models.CharField(max_length=20)
    last_name =  models.CharField(max_length=20)
    email = models.EmailField(max_length=30, null=True)
    dob = models.DateField(null=True)

    def __str__(self):
        return f"Passenger: {self.first_name} {self.last_name}"
    
class Ticket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    depart_flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='depart')
    return_flight = models.ForeignKey(Flight, on_delete=models.CASCADE, null=True, default=None,  related_name='return_ticket')
    passengers = models.ManyToManyField(Passenger)
    total_cost = models.DecimalField(max_digits=8, decimal_places=2)
    seatClass = models.CharField(max_length=20, default="Economy")
    date_created = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.passengers} - {self.depart_flight}"
    
    def updateSeatClass(self, newSeatClass):
        self.seatClass = newSeatClass

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birthdate = models.DateField(null=True, blank=True)
    street_address = models.CharField(max_length=255, null=True, blank=True)
    zip_code = models.CharField(max_length=10, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
