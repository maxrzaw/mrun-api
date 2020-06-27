from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import Comment, Workout, Activity

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'year']

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'activity', 'time', 'text']

class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'title', 'description', 'category', 'owner']


class ActivitySummarySerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer()
    class Meta:
        model = Activity
        fields = ['id', 'user', 'workout_id', 'time', 'comment', 'workout']

class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'workout_id', 'time', 'comment']