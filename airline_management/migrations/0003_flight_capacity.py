# Generated by Django 5.0.3 on 2024-03-19 13:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("airline_management", "0002_flight"),
    ]

    operations = [
        migrations.AddField(
            model_name="flight",
            name="capacity",
            field=models.IntegerField(default=2),
            preserve_default=False,
        ),
    ]
