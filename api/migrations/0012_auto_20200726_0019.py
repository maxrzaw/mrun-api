# Generated by Django 3.0.8 on 2020-07-26 00:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_workout_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
