# Generated by Django 3.0.6 on 2020-07-10 00:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20200710_0040'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='memberships',
            constraint=models.UniqueConstraint(fields=('user',), name='unique-user'),
        ),
    ]
