"""API URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import include, path
from rest_framework.authtoken.views import obtain_auth_token

from api import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('token-auth/', obtain_auth_token, name='api-token-auth'),
    path('register/', views.Register.as_view(), name='register-view'),
    path('groups/', views.GroupList.as_view(), name='group-list'),
    path('groups/<int:group_id>/', views.GroupDetail.as_view(), name='group-detail'),
    path('groups/<int:group_id>/members/', views.GroupMembers.as_view(), name='group-members'),
    path('users/', views.UserList.as_view(), name='user-list'),
    path('users/<int:user_id>/', views.UserDetail.as_view(), name='user-detail'),
    path('users/<int:user_id>/activities/', views.UserActivities.as_view(), name='user-activities'),
    path('users/<int:user_id>/workouts/', views.UserWorkouts.as_view(), name='user-workouts'),
    path('comments/', views.CommentList.as_view(), name='comment-list'),
    path('comments/<int:comment_id>/', views.CommentDetail.as_view(), name='comment-detail'),
    path('workouts/', views.WorkoutList.as_view(), name='workout-list'),
    path('workouts/<int:workout_id>/', views.WorkoutDetail.as_view(), name='workout-detail'),
    path('activities/', views.ActivityList.as_view(), name='activity-list'),
    path('activities/<int:activity_id>/', views.ActivityDetail.as_view(), name='activity-detail'),
    path('activities/<int:activity_id>/comments/', views.ActivityComments.as_view(), name='activity-comments'),
    path('suggestions/', views.SuggestionView.as_view(), name='suggestions'),
    path('suggestions/<int:sid>/', views.SuggestionDetail.as_view(), name='suggestions-detail'),
    path('membership/', views.Membership.as_view(), name='membership'),
    path('credential-check/', views.CredentialCheck.as_view(), name='credential-check'),
    path('me/', views.Me.as_view(), name='me'),
    path('', views.index, name='api-index'),
]


