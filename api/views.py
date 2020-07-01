from rest_framework import viewsets # Don't want this later
from rest_framework import permissions
from api.permissions import CustomCommentPermission, IsAdminOrReadOnly, IsOwnerAdminOrReadOnly
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.serializers import UserSerializer, GroupSerializer, CommentSerializer, ActivitySerializer, WorkoutSerializer, ActivitySummarySerializer
from api.models import Comment, Workout, Activity, Group, Memberships
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
import json
User = get_user_model()

class UserList(APIView):
    """
    API endpoint that allows users to be viewed.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        params = request.query_params
        page = int(params.get("page", 1)) # default page number is 1
        per_page = int(params.get("per_page", 10)) # default per page is 10
        # Get all the Users
        users = User.objects.all().order_by('id')
        paginator = Paginator(users, per_page, allow_empty_first_page=True)

        try:
            # Get requested page
            requested_page = paginator.page(page)
        except InvalidPage:
            raise Http404("Invalid Page")
        # Serialize requested page and return
        serializer = UserSerializer(requested_page, many=True)
        renderer = JSONRenderer()
        data = {}

        user_list = renderer.render(serializer.data).decode('utf-8')
        data["users"] = json.loads(user_list)
        data["next"] = requested_page.next_page_number() if requested_page.has_next() else None

        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)


class UserDetail(APIView):
    """
    API endpoint that allows view of one user.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id, format=None):
        # get the User object
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)

        fields = ['id', 'username', 'first_name', 'last_name', 'bio', 'year']
        # Turn it into a dictionary for JsonResponse
        dict_obj = model_to_dict(user, fields=fields)
        return JsonResponse(dict_obj, status=status.HTTP_200_OK)

    
class UserActivities(APIView):
    """
    API endpoint for viewing a users activities.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id, format=None):
        params = request.query_params
        page = int(params.get("page", 1)) # default page number is 1
        per_page = int(params.get("per_page", 10)) # default per page is 10
        sort = params.get("sort", "desc")
        sort = '-time' if sort == "desc" else 'time'

        # Check if the user exists
        try:
            # get the user object
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)

        # Get the Activities
        activities = Activity.objects.filter(user=user_id).order_by(sort)
        # Create the paginator
        paginator = Paginator(activities, per_page, allow_empty_first_page=True)

        try:
            # Get requested page
            requested_page = paginator.page(page)
        except InvalidPage:
            raise Http404("Invalid page.")
        # Serialize requested page and return
        serializer = ActivitySummarySerializer(requested_page, many=True)

        renderer = JSONRenderer()
        activity_list = renderer.render(serializer.data).decode('utf-8')
        data = {}
        data["user"] = user_id
        data["activities"] = json.loads(activity_list)
        data["next"] = requested_page.next_page_number() if requested_page.has_next() else None

        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)


class UserWorkouts(APIView):
    """
    API endpoint for viewing a users workouts.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, user_id, format=None):
        params = request.query_params
        page = int(params.get("page", 1)) # default page number is 1
        per_page = int(params.get("per_page", 10)) # default per page is 10
        workout_type = params.get("type", None)

        # Check if the user exists
        try:
            # get the user object
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)

        # Get the Workouts
        workouts = Workout.objects.filter(owner=user_id).order_by('id') if workout_type is None else Workout.objects.filter(owner=user_id, category=workout_type).order_by('id')
        # Create the paginator
        paginator = Paginator(workouts, per_page, allow_empty_first_page=True)
        try:
            # Get requested page
            requested_page = paginator.page(page)
        except InvalidPage:
            raise Http404("Invalid Page")
        # Serialize requested page and return
        serializer = WorkoutSerializer(requested_page, many=True)

        renderer = JSONRenderer()
        workout_list = renderer.render(serializer.data).decode('utf-8')
        data = {}
        data["user"] = user_id
        data["workouts"] = json.loads(workout_list)
        data["next"] = requested_page.next_page_number() if requested_page.has_next() else None

        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)


class CommentList(APIView):
    """
    List all comments or create a new one.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        params = request.query_params
        page = int(params.get("page", 1)) # default page number is 1
        per_page = int(params.get("per_page", 10)) # default per page is 10
        # Get all the comments
        all_comments = Comment.objects.all().order_by('id')

        # Create a paginator
        paginator = Paginator(all_comments, per_page, allow_empty_first_page=True)

        try:
            # Get requested page
            requested_page = paginator.page(page)
        except InvalidPage:
            raise Http404("Invalid Page")
        # Serialize requested page and return
        serializer = CommentSerializer(requested_page, many=True)
        renderer = JSONRenderer()
        data = {}
        
        comment_list = renderer.render(serializer.data).decode('utf-8')
        data["comments"] = json.loads(comment_list)

        data["next"] = requested_page.next_page_number() if requested_page.has_next() else None
        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)


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

    permission_classes = [CustomCommentPermission]

    def get(self, request, comment_id, format=None):
        try:
            # get the comment object
            comment = Comment.objects.get(id=comment_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)
        
        # check the comment permissions
        self.check_object_permissions(request, comment)
        # Turn it into a dictionary for JsonResponse
        dict_obj = model_to_dict(comment)
        return JsonResponse(dict_obj, status=status.HTTP_200_OK)

    def patch(self, request, comment_id, format=None):
        try:
            # get the comment object
            comment = Comment.objects.get(id=comment_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)
        # check the comment permissions
        self.check_object_permissions(request, comment)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, comment_id, format=None):
        try:
            # get the comment object
            comment = Comment.objects.get(id=comment_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)
        # check the comment permissions
        self.check_object_permissions(request, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class GroupList(APIView):
    """
    API endpoint for viewing a list of all the groups.
    """
    permission_classes = [IsAdminOrReadOnly]
    def get(self, request, format=None):
        groups = Group.objects.all()
        serializer = GroupSerializer(groups, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # Get the data from the request
        data = request.data
        
        serializer = GroupSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GroupDetail(APIView):
    """
    API endpoint for viewing a single group.
    """
    permission_classes = [permissions.IsAdminUser]

    def patch(self, request, group_id, format=None):
        try:
            # Get the group
            group = Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            raise Http404("Group does not exist.")
        serializer = GroupSerializer(group, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, group_id, format=None):
        try:
            # Get the group
            group = Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            raise Http404("Group does not exist.")
        group.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class GroupMembers(APIView):
    """
    API endpoint to view the member list of a group.
    """
    permission_classes = [permissions.IsAdminUser]
    def get(self, request, group_id, format=None):

        try:
            # Get the group
            group = Group.objects.get(id=group_id)
        except ObjectDoesNotExist:
            raise Http404("Group does not exist.")

        members = list()
        for m in Memberships.objects.filter(group_id=group_id).select_related('user'):
            members.append(m.user)
        serializer = UserSerializer(members, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WorkoutList(APIView):
    """
    API endpoint for list of workouts.
    """
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, format=None):
        params = request.query_params
        page = int(params.get("page", 1)) # default page number is 1
        per_page = int(params.get("per_page", 10)) # default per page is 10
        category = params.get("type", None)

        # Retrieve the workouts
        workouts = Workout.objects.all().order_by('id') if category is None else Workout.objects.filter(category=category).order_by('id')

        # Create the paginator
        paginator = Paginator(workouts, per_page, allow_empty_first_page=True)

        try:
            # Get requested page
            requested_page = paginator.page(page)
        except InvalidPage:
            raise Http404("Invalid Page")
        # Serialize requested page and return
        serializer = WorkoutSerializer(requested_page, many=True)

        renderer = JSONRenderer()
        workout_list = renderer.render(serializer.data).decode('utf-8')
        data = {}
        data["workouts"] = json.loads(workout_list)
        data["next"] = requested_page.next_page_number() if requested_page.has_next() else None

        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)


    def post(self, request, format=None):
        # Modify the data a little
        data = request.data
        data["owner"] = request.user.id
        
        serializer = WorkoutSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class WorkoutDetail(APIView):
    """
    API endpoint for viewing a single workout.
    """

    permission_classes = [IsOwnerAdminOrReadOnly]

    def get(self, request, workout_id, format=None):
        try:
            # Get the workout
            workout = Workout.objects.get(id=workout_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)

        # Check permissions 
        self.check_object_permissions(request, workout)

        serializer = WorkoutSerializer(workout)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, workout_id, format=None):
        data = request.data

        try:
            # Get the workout
            workout = Workout.objects.get(id=workout_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)

        # Check permissions 
        self.check_object_permissions(request, workout)

        serializer = WorkoutSerializer(workout, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, workout_id, format=None):
        try:
            # Get the workout
            workout = Workout.objects.get(id=workout_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)

        # Check permissions 
        self.check_object_permissions(request, workout)

        workout.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        params = request.query_params
        page = int(params.get("page", 1)) # default page number is 1
        per_page = int(params.get("per_page", 10)) # default per page is 10
        category = params.get("type", None)

        if type is None:
            activities = Activity.objects.all()
            
        else:
            all_activities = Activity.objects.select_related('workout')
            activities = list()
            for a in all_activities:
                if a.workout.category == category:
                    activities.append(a)
        paginator = Paginator(activities, per_page, allow_empty_first_page=True)

        try:
            # Get requested page
            requested_page = paginator.page(page)
        except InvalidPage:
            raise Http404("Invalid Page")
        # Serialize requested page and return
        serializer = ActivitySummarySerializer(data=requested_page, many=True)

        renderer = JSONRenderer()
        activity_list = renderer.render(serializer.data).decode('utf-8')

        data = {}
        data["activities"] = json.loads(activity_list)
        data["next"] = requested_page.next_page_number() if requested_page.has_next() else None
        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)

    def post(self, request, format=None):
        params = request.query_params
        new_workout = params.get("new_workout", 0)

        data = request.data
        data["user"] = request.user.id

        if new_workout:
            # Use the ActivitySummarySerializer

            # Check if 'workout" key is missing
            if "workout" not in data:
                raise Http404('Missing "workout" key')

            # Add "owner" field to data["workout"]
            data["workout"]["owner"] = data["user"]

            serializer = ActivitySummarySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                raise Http404(serializer.errors)
        else:
            # Use the ActivitySerializer
            serializer = ActivitySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)




    