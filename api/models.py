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
    

class Group(models.Model):
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()

class Memberships(models.Model):
    user = models.ForeignKey('api.User', on_delete=models.CASCADE)
    group = models.ForeignKey('api.Group', on_delete=models.CASCADE)

class Workout(models.Model):
    workout_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    creator = models.ForeignKey('api.User', on_delete=models.DO_NOTHING, null=True)

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
    athlete = models.ForeignKey('api.User', on_delete=models.CASCADE)
    workout = models.ForeignKey('api.Workout', on_delete=models.PROTECT)
    time = models.DateTimeField(auto_now_add=True, editable=False)
    comment = models.TextField(default='')

class Suggestion(models.Model):
    group = models.ForeignKey('api.Group', on_delete=models.CASCADE)
    workout = models.ForeignKey('api.Workout', on_delete=models.CASCADE)
    date = models.DateField()


class Follows(models.Model):
    """
    User 1 follows user 2.
    This is a one way relationship.
    """
    user1 = models.ForeignKey('api.User', on_delete=models.CASCADE, related_name='follower')
    user2 = models.ForeignKey('api.User', on_delete=models.CASCADE)