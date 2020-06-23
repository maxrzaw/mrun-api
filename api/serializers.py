from django.contrib.auth.models import Group
from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import Comment

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'url', 'username', 'first_name', 'last_name', 'email', 'bio', 'year']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'activity', 'time', 'text']