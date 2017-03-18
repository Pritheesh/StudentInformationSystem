from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views
from InfoSystem import api_views
from InfoSystem import serializers_views as s_views
from InfoSystem import views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    # url(r'^api/register/$', api_views.register, name='api-register'),
    # url(r'^api/login/$', api_views.login_user, name='api-login'),
    # url(r'^$', views.index, name='home'),
    url(r'^accounts/login/$', api_views.login_user, name='login'),
    # url(r'^api/logout/$', api_views.logout_view, name='api-logout'),
    url(r'^api/results/$', s_views.StudentList.as_view()),
    url(r'^api/register/$', s_views.UserRegisterView.as_view(), name='api-register'),
    # url(r'^api/register/student', s_views.StudentRegisterView.as_view(), name='api-student-register'),


    # url(r'^results/$', api_views.result_view, name='result-view'),
    url(r'^login/$', auth_views.login, {'redirect_authenticated_user': True}, name='login'),
    url(r'^register/$', views.register, name='register'),
    url(r'^results/$', login_required(views.result_view), name='result-view'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
