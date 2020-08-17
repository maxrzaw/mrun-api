from rest_framework import viewsets # Don't want this later
from rest_framework import permissions
from api.permissions import CustomCommentPermission, IsAdminOrReadOnly, IsOwnerAdminOrReadOnly, IsUserAdminOrReadOnly
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from api.serializers import *
from api.models import Comment, Workout, Activity, Group, Memberships, Suggestion
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.contrib.auth import get_user_model
from django.forms.models import model_to_dict
from django.shortcuts import render
import json
import datetime
import django.contrib.auth.password_validation as password_validation
from rest_framework.authtoken.models import Token
User = get_user_model()

def index(request):
    return render(request, 'api/index.html')

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
        serializer = ActivityFullSerializer(requested_page, many=True)

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
        workouts = Workout.objects.filter(owner=user_id, deleted=False).order_by('id') if workout_type is None else Workout.objects.filter(owner=user_id, category=workout_type, deleted=False).order_by('id')
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
        
        serializer = CreateCommentSerializer(data=data)
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
        workouts = Workout.objects.filter(deleted=False).order_by('id') if category is None else Workout.objects.filter(category=category, deleted=False).order_by('id')

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
        workout.deleted = True
        workout.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        params = request.query_params
        page = int(params.get("page", 1)) # default page number is 1
        per_page = int(params.get("per_page", 10)) # default per page is 10
        filter = params.get("filter", None)
        sort = params.get("sort", "desc") # default is descending
        sort = '-time' if sort == "desc" else 'time'



        if filter == "group":
            try: 
                membership = Memberships.objects.get(user_id=request.user.id)
                group = membership.group_id
                results = Memberships.objects.filter(group_id=group)
                
                users = []
                for m in results:
                    users.append(m.user_id)
                
                activities = Activity.objects.filter(user__in=users).order_by(sort)
            except ObjectDoesNotExist as error:
                return Response(data={"detail": "User not in group."}, status=status.HTTP_400_BAD_REQUEST)

        elif filter is None:
            activities = Activity.objects.all().order_by(sort)
            
        else:
            all_activities = Activity.objects.select_related('workout').order_by(sort)
            activities = list()
            for a in all_activities:
                if a.workout.category == filter:
                    activities.append(a)

        paginator = Paginator(activities, per_page, allow_empty_first_page=True)

        try:
            # Get requested page
            requested_page = paginator.page(page)
        except InvalidPage:
            raise Http404("Invalid Page")
        # Serialize requested page and return
        serializer = ActivityFullSerializer(data=requested_page, many=True)
        #serializer = ActivitySummarySerializer(data=requested_page, many=True)
        serializer.is_valid()

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


class ActivityDetail(APIView):
    """
    API endpoint for viewing and editing activities.
    """
    permission_classes = [IsUserAdminOrReadOnly]

    def get(self, request, activity_id, format=None):
        try:
            # Get the activity
            activity = Activity.objects.get(id=activity_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)
        
        # Check permission
        self.check_object_permissions(request, activity)
        serializer = ActivityFullSerializer(activity)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, activity_id, format=None):
        data = request.data
        try:
            # Get the activity
            activity = Activity.objects.get(id=activity_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)

        # Check permission
        self.check_object_permissions(request, activity)
        serializer = ActivitySummarySerializer(activity, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_406_NOT_ACCEPTABLE)
        
    def delete(self, request, activity_id, format=None):
        try:
            # Get the activity
            activity = Activity.objects.get(id=activity_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)

        # Check permission
        self.check_object_permissions(request, activity)
        activity.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ActivityComments(APIView):
    """
    API endpoint for getting comments on an activity.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, activity_id, format=None):
        # Check that workout exists
        # get pagnation params
        # return list
        params = request.query_params
        page = int(params.get("page", 1)) # default page number is 1
        per_page = int(params.get("per_page", 10)) # default per page is 10

        # Check to make sure group is valid
        if not Activity.objects.filter(id=activity_id).exists():
            return Response(data={"detail": "Invalid activity id."}, status=status.HTTP_400_BAD_REQUEST)
        
        comments = Comment.objects.filter(activity_id=activity_id).order_by('id')

        paginator = Paginator(comments, per_page, allow_empty_first_page=True)


        try:
            # Get requested page
            requested_page = paginator.page(page)
        except InvalidPage:
            raise Http404("Invalid Page")
        # Serialize requested page and return
        serializer = CommentSerializer(data=requested_page, many=True)
        serializer.is_valid()

        renderer = JSONRenderer()
        comment_list = renderer.render(serializer.data).decode('utf-8')

        data = {}
        data["comments"] = json.loads(comment_list)
        data["next"] = requested_page.next_page_number() if requested_page.has_next() else None
        return JsonResponse(data, status=status.HTTP_200_OK, safe=False)




class SuggestionView(APIView):
    """
    API endpoint for suggested workouts.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, format=None):
        params = request.query_params
        # default group of 1
        group = params.get("group", 'all')
        # default date of today
        date = params.get("date", datetime.date.today())

        if group == 'all':
            try:
                # Get the workout
                suggestions = Suggestion.objects.select_related('workout').filter(date=date)
            except ObjectDoesNotExist as err:
                raise Http404(err)
            # convert to a workout
            serializer = SuggestionSummarySerializer(suggestions, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                # Get the workout
                suggestion = Suggestion.objects.select_related('workout').get(group_id=group, date=date)
            except ObjectDoesNotExist as err:
                raise Http404(err)
            # convert to a workout
            workout = suggestion.workout
            serializer = WorkoutSerializer(workout)
            return Response(data=serializer.data, status=status.HTTP_200_OK)



    def post(self, request, format=None):
        data = request.data
        if Suggestion.objects.filter(group=data['group'], date=data['date']).exists():
            print('Hi')
            return Response(data='{ "detail": "Suggestion already exists on this day and group." }', status=status.HTTP_409_CONFLICT)
        serializer = SuggestionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            print(serializer.errors)
            raise Http404(serializer.errors)

class SuggestionDetail(APIView):
    """
    API endpoint for suggested workouts.
    """
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, sid, format=None):
        
        try:
            # Get the workout
            suggestion = Suggestion.objects.select_related('workout').get(id=sid)
        except ObjectDoesNotExist as err:
            raise Http404(err)


        serializer = SuggestionSummarySerializer(suggestion)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, sid, format=None):
        try:
            # Get the workout
            suggestion = Suggestion.objects.select_related('workout').get(id=sid)
        except ObjectDoesNotExist as err:
            raise Http404(err)

        suggestion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Register(APIView):
    """
    API endpoint for creating a new user.
    """

    def post(self, request, format=None):
        """
        Need:
        Matching passwords
        First and last name
        unique email

        """
        data = request.data

        validated_data = {}
        # Required fields
        if not "email" in data:
            return Response(data='{ "detail": "email not provided." }', status=status.HTTP_403_FORBIDDEN)
        if not "username" in data:
            return Response(data='{ "detail": "username not provided." }', status=status.HTTP_403_FORBIDDEN)
        if not "password1" in data:
            return Response(data='{ "detail": "password1 not provided." }', status=status.HTTP_403_FORBIDDEN)
        if not "password2" in data:
            return Response(data='{ "detail": "password2 not provided." }', status=status.HTTP_403_FORBIDDEN)
        
        validated_data["email"] = data["email"]
        validated_data["username"] = data["username"]
        validated_data["password1"] = data["password1"]
        validated_data["password2"] = data["password2"]
        # required but has a default
        validated_data["year"] = data.get("year", 'FR')

        # Optional fields
        validated_data["first_name"] = data.get("first_name", '')
        validated_data["last_name"] = data.get("last_name", '')
        validated_data["bio"] = data.get("bio", '')
        

        # Check if email is used
        if User.objects.filter(email=data["email"]).exists():
            return Response(data='{ "detail": "email already in use." }', status=status.HTTP_403_FORBIDDEN)

        # Check if username is used
        if User.objects.filter(username=data["username"]).exists():
            return Response(data='{ "detail": "username already in use." }', status=status.HTTP_403_FORBIDDEN)
        
        # Check to make sure passwords match
        if data["password1"] != data["password2"]:
            return Response(data='{ "detail": "passwords must match." }', status=status.HTTP_403_FORBIDDEN)

        try:
            password_validation.validate_password(data["password1"])
            serializer = CreateUserSerializer(data=validated_data)
            if serializer.is_valid():
                new_user = serializer.save()
                new_user.set_password(data["password1"])
                new_user.save()
                token = Token.objects.get_or_create(user=new_user)
                return Response({'token': token[0].key}, status=status.HTTP_201_CREATED)
        except password_validation.ValidationError as err:
            return Response(data=err, status=status.HTTP_403_FORBIDDEN)

class Membership(APIView):
    """
    API endpoint for joining (or switching) groups.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        try:
            group_id = request.query_params.get("group", None)
        except AttributeError:
            return Response(data={"detail": "Missing group parameter."}, status=status.HTTP_400_BAD_REQUEST)

        if group_id is None:
            return Response(data={"detail": "Missing group parameter."}, status=status.HTTP_400_BAD_REQUEST)

        user_id = request.user.id
        # Check to make sure group is valid
        if not Group.objects.filter(id=group_id).exists():
            return Response(data={"detail": "Invalid group id."}, status=status.HTTP_400_BAD_REQUEST)

        
        # Check if the user already has a group
        if Memberships.objects.filter(user_id=user_id).exists():
            entry = Memberships.objects.get(user_id=user_id)
            entry.group_id = group_id
            entry.save()
            serializer = MembershipSerializer(entry)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            data = { "group": group_id, "user": user_id }
            serializer = NewMembershipSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                group = Group.objects.get(id=group_id)
                cereal = GroupSerializer(group)
                data = {'user': user_id, 'group': cereal.data}

                return Response(data=data, status=status.HTTP_200_OK)
            else:
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        # get query params and default to logged in user
        params = request.query_params
        user_id = params.get("user", request.user.id)

        # get the User object
        try:
            user = User.objects.get(id=user_id)
        except ObjectDoesNotExist as err:
            raise Http404(err)
        # get the entry of the logged in user
        try: 
            membership = Memberships.objects.get(user_id=user.id)
            serializer = MembershipSerializer(membership)
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except ObjectDoesNotExist as error:
            # Lets return group 1
            group = Group.objects.get(id=1)
            cereal = GroupSerializer(group)
            data = {'user': user_id, 'group': cereal.data}
            return Response(data=data, status=status.HTTP_200_OK)

class CredentialCheck(APIView):
    """
    API endpoint for checking if authenticated.
    """
    permission_classes = [permissions.IsAuthenticated]

    def head(self, request, format=None):
        return Response(status=status.HTTP_204_NO_CONTENT)

class Me(APIView):
    """
    Returns the current logged in user.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        serializer = AdvancedUserSerializer(request.user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, format=None):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    







        






    
