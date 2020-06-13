from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    bio = models.TextField(max_length=500, blank=True)
    YEAR_IN_SCHOOL_CHOICES = [
        ('FR', 'Freshman'),
        ('SO', 'Sophomore'),
        ('JR', 'Junior'),
        ('SR', 'Senior'),
        ('GR', 'Graduate'),
    ]
    year = models.CharField(
        max_length=2,
        choices=YEAR_IN_SCHOOL_CHOICES,
        default='FR',
    )
    GROUP_CHOICES = [
        ('SH', 'Short Sprints'),
        ('LO', 'Long Sprints'),
        ('DI', 'Distance Scrubs'),
    ]
    group = models.CharField(
        max_length=2,
        choices=GROUP_CHOICES,
        default='LO',
    )

class Workout(models.Model):
    workout_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    HILL = 'H'
    CORE = 'C'
    TRACK = 'T'
    SPEED = 'S'
    LONG = 'L'
    CATEGORY_CHOICES = [
        (TRACK, 'Track'),
        (SPEED, 'Speed'),
        (HILL, 'Hill'),
        (LONG, 'Long'),
        (CORE, 'Core'),
    ]

    category = models.CharField(
        max_length=1, 
        choices=CATEGORY_CHOICES,
        default=TRACK)

class Activity(models.Model):
    athlete = models.ForeignKey('api.User', on_delete=models.CASCADE, )