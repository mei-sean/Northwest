from django.db import models

class Airport(models.Model):
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Flight(models.Model):
    flight_number = models.IntegerField()
    depart_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='depart_flight')
    destination_airport = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='destination_flight')
    departure_date = models.DateField()
    number_of_seats = models.IntegerField()
    depart_time = models.TimeField()


    def __str__(self):
        return f"{self.source_airport} to {self.destination_airport}"
# Create your models here.


# Create your models here.
