from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'year']


class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'username', 'first_name', 'last_name', 'bio', 'year']

class UserSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name']

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'description']


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
    
    def create(self, validated_data):
        workout_data = validated_data.pop('workout')
        workout = Workout.objects.create(**workout_data)
        activity = Activity.objects.create(workout=workout, **validated_data)
        return activity


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'workout_id', 'time', 'comment']

class SuggestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestion
        fields = ['id', 'group', 'workout_id', 'date']

class SuggestionSummarySerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer()
    class Meta:
        model = Suggestion
        fields = ['id', 'workout_id', 'date', 'workout']

class MembershipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Memberships
        fields = ['user', 'group']

