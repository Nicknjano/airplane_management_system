# Generated by Django 5.0.3 on 2024-03-27 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('airline_management', '0013_route_seats_remaining'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='payment_status',
            field=models.CharField(choices=[('not_paid', 'Not Paid'), ('paid', 'Paid')], default='paid', max_length=20),
        ),
    ]