# Generated by Django 5.0.6 on 2024-05-25 16:08

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("theatre", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ticket",
            name="reservation",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="tickets",
                to="theatre.reservation",
            ),
        ),
        migrations.AddConstraint(
            model_name="ticket",
            constraint=models.UniqueConstraint(
                fields=("seat", "performance"),
                name="unique_ticket_seat_performance",
            ),
        ),
    ]
