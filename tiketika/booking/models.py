from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Bus(models.Model):
    company = models.CharField(max_length=55, null=True)
    bus_no = models.CharField(max_length=30, null=False)
    bus_name = models.CharField(max_length=30, null=False)
    total_seats = models.IntegerField(null=False)
    contact = models.IntegerField(null=False)

    def __str__(self):
        return self.bus_name


class Passenger(models.Model):
    name = models.CharField(max_length=55, null=False)
    phone = models.IntegerField(null=False)
    email = models.EmailField(max_length=50, blank=True)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True)
    seat_no = models.IntegerField(null=True)

    def __str__(self):
        return self.name

class Route(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    source = models.CharField(max_length=20, null=False)
    destination = models.CharField(max_length=20, null=False)
    fares = models.IntegerField(null=False)
    journey_date = models.DateField(null=False)
    departure = models.TimeField(null=False)
    arrival = models.TimeField(null=False)
    
    def __str__(self):
        return self.source + ' - ' + self.destination
    
    def save(self, *args, **kwargs):
        self.source = self.source.lower()
        self.destination = self.destination.lower()
        super(Route, self).save(*args, **kwargs)

        
#class Seat(models.Model):
 #   bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
  #  passenger = models.CharField(max_length=55, null=True)
   # seat_no = models.IntegerField(null=True)


class Booking(models.Model):
    Booked = 'B'
    Cancelled = 'C'
    BOOK_STATUS = (
        ('B', 'Booked'),
		('C', 'Cancelled'),
        )
    passenger = models.CharField(max_length=55, null=True)
    phone = models.IntegerField(null=True)
    bus = models.CharField(max_length=55, null=True)
    journey_date = models.DateField(null=False)
    departure = models.TimeField(null=False)
    arrival = models.TimeField(null=False)
    source = models.CharField(max_length=55, null=True)
    fare = models.IntegerField(null=True)
    destination = models.CharField(max_length=55, null=True)
    seat_no = models.IntegerField(null=True)
    status = models.CharField(choices=BOOK_STATUS, default=Booked, max_length=1)
    complete = models.BooleanField(default=False, null=True)

    def __str__(self):
        return self.passenger

class Faq(models.Model):
    name = models.CharField(max_length=50, null=True)
    question = models.TextField(max_length=300, null=True)
    answer = models.TextField(max_length=200, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    name = models.CharField(max_length=50, null=True)
    review = models.TextField(max_length=200, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length=50, null=True)
    message = models.TextField(max_length=300, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


