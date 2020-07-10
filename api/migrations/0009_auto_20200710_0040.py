# Generated by Django 3.0.6 on 2020-07-10 00:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_auto_20200627_2127'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='suggestion',
            constraint=models.UniqueConstraint(fields=('group', 'date'), name='unique-group-date'),
        ),
    ]