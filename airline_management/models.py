from django.db import models

# class Booking(models.Model):
#     class_choices = (
#         ('Economy', 'Economy'),
#         ('Business', 'Business'),
#         ('First', 'First'),
#     )

#     from_choices = (
#         ('Nairobi', 'Nairobi'),
#         ('Kisumu', 'Kisumu'),
#         ('Mombasa', 'Mombasa'),
#         ('California', 'California'),
#         ('NewYork', 'New York'),
#         ('Michigan', 'Michigan'),
#     )

#     class_field = models.CharField(max_length=10, choices=class_choices)
#     from_field = models.CharField(max_length=20, choices=from_choices)
#     to_field = models.CharField(max_length=20, choices=from_choices)
#     departure_date = models.DateField()
#     return_date = models.DateField()
#     adults = models.IntegerField()
#     children = models.IntegerField()
#     price = models.IntegerField()

#     def save(self, *args, **kwargs):
#         # Assign price based on destination
#         price_dict = {
#             ('Nairobi', 'Kisumu'): 100,
#             ('Nairobi', 'Mombasa'): 200,
#             ('Nairobi', 'California'): 8000,
#             ('Nairobi', 'NewYork'): 2000,
#             ('Nairobi', 'Michigan'): 200,
#             ('Kisumu', 'Nairobi'): 100,
#             ('Kisumu', 'Mombasa'): 200,
#             ('Kisumu', 'California'): 8000,
#             ('Kisumu', 'NewYork'): 2000,
#             ('Kisumu', 'Michigan'): 200,
#             ('Mombasa', 'Kisumu'): 200,
#             ('Mombasa', 'Nairobi'): 200,
#             ('Mombasa', 'California'): 8000,
#             ('Mombasa', 'NewYork'): 2000,
#             ('Mombasa', 'Michigan'): 200,
#             ('California', 'Kisumu'): 100,
#             ('California', 'Mombasa'): 200,
#             ('California', 'Nairobi'): 8000,
#             ('California', 'NewYork'): 2000,
#             ('California', 'Michigan'): 200,
#             ('NewYork', 'Kisumu'): 100,
#             ('NewYork', 'Mombasa'): 200,
#             ('NewYork', 'California'): 8000,
#             ('NewYork', 'Nairobi'): 2000,
#             ('NewYork', 'Michigan'): 200,
#             ('Michigan', 'Kisumu'): 100,
#             ('Michigan', 'Mombasa'): 200,
#             ('Michigan', 'California'): 8000,
#             ('Michigan', 'NewYork'): 2000,
#             ('Michigan', 'Nairobi'): 200,
#         }
#         if (self.from_field, self.to_field) in price_dict:
#             self.price = price_dict[(self.from_field, self.to_field)]
#         super().save(*args, **kwargs)


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

    class_type = models.CharField(max_length=100, choices=CLASS_CHOICES, default='Economy')
    origin = models.CharField(max_length=100,default='')
    destination = models.CharField(max_length=100,default='')
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    adults = models.IntegerField(default=1)
    children = models.IntegerField(default=0)


class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Assuming price is in decimal format

    def __str__(self):
        return f"{self.origin} to {self.destination}"
