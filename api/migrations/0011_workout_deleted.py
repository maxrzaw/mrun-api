# Generated by Django 3.0.8 on 2020-07-17 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20200710_0050'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='deleted',
            field=models.BooleanField(default=False),
        ),
    ]