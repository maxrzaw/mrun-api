from rest_framework import viewsets # Don't want this later
from rest_framework import permissions
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.decorators import api_view # Probably don't want this
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer, CommentSerializer # These seem kinda dumb
from api.models import Comment
from django.contrib.auth.models import Group
from django.http import Http404
from django.contrib.auth import get_user_model
User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class CommentList(APIView):
    """
    List all comments or create a new one.
    """

    def get(self, request, format=None):
        all_comments = Comment.objects.all()
        serializer = CommentSerializer(all_comments, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        # Modify the data a little
        data = request.data
        data["user"] = request.user.id
        
        serializer = CommentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(APIView):
    """
    Modify, delete, or get a specific comment.
    """

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAdminUser]