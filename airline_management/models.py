from django.db import models

class Flight(models.Model):
    flight_number = models.IntegerField()
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    departure_date = models.DateField()
    departure_time = models.TimeField()
    journey_hours = models.IntegerField()
    intervals = models.IntegerField()
    capacity = models.IntegerField()


class Airbus(models.Model):
    airbus_no = models.IntegerField(unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f"Airbus {self.airbus_no}"

class Booking(models.Model):
    CLASS_CHOICES = [
        ('Economy', 'Economy'),
        ('Business', 'Business'),
        ('First', 'First'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('not_paid', 'Not Paid'),
        ('paid', 'Paid'),
    ]

    class_type = models.CharField(max_length=100, choices=CLASS_CHOICES, default='Economy')
    origin = models.CharField(max_length=100,default='')
    destination = models.CharField(max_length=100,default='')
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    email = models.EmailField()
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='not_paid')

    def save(self, *args, **kwargs):
        # Save the email of the first person if it's not already set
        if not self.email:
            # Assuming the email of the first person is stored in the first passenger's email field
            first_passenger_email = self.passenger_set.first().email
            self.email = first_passenger_email
        super().save(*args, **kwargs)


class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Assuming price is in decimal format

    def __str__(self):
        return f"{self.origin} to {self.destination}"
