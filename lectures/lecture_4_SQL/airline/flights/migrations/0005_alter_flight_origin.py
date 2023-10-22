# Generated by Django 4.2.4 on 2023-09-01 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("flights", "0004_rename_passanger_passenger"),
    ]

    operations = [
        migrations.AlterField(
            model_name="flight",
            name="origin",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="departures",
                to="flights.airport",
            ),
        ),
    ]