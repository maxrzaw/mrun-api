"""
mrun_api URL Configuration
"""
from django.contrib import admin
from django.conf.urls import url
from django.urls import include, path
from django.contrib.auth import views as auth_views
from mrun_api import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('v1/', include('api.urls'), name='api-root'),
    path('admin/', admin.site.urls),
    path('', views.index_view, name ='index'),
]


