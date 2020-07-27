from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'year']

class AdvancedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'year', 'is_staff']


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
    user = UserSummarySerializer()
    class Meta:
        model = Comment
        fields = ['id', 'user', 'activity', 'time', 'text']

class CreateCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'activity', 'text']


class WorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workout
        fields = ['id', 'title', 'description', 'category', 'owner', 'deleted']


class ActivitySummarySerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer()
    class Meta:
        model = Activity
        fields = ['id', 'user', 'time', 'comment', 'workout']
    
    def create(self, validated_data):
        workout_data = validated_data.pop('workout')
        workout = Workout.objects.create(**workout_data)
        activity = Activity.objects.create(workout=workout, **validated_data)
        return activity

class ActivityFullSerializer(serializers.ModelSerializer):
    workout = WorkoutSerializer()
    user = UserSummarySerializer()
    class Meta:
        model = Activity
        fields = ['id', 'user', 'time', 'comment', 'workout']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'user', 'workout', 'time', 'comment']

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
    group = GroupSerializer()
    class Meta:
        model = Memberships
        fields = ['user', 'group']

