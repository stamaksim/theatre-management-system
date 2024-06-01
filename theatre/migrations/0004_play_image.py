# Generated by Django 5.0.6 on 2024-05-30 15:05

import theatre.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('theatre', '0003_alter_ticket_reservation_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='play',
            name='image',
            field=models.ImageField(null=True, upload_to=theatre.models.play_image_file_path),
        ),
    ]