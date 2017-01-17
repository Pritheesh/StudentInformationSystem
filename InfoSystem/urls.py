from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from InfoSystem import views
from InfoSystem import serializers_views as s_views
from rest_framework.authtoken import views as rest_views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^$', views.index, name='home'),
    url(r'^accounts/login/$', views.login_user, name='login'),
    url(r'^results/$', views.result_view, name='result-view'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^api/results/$', s_views.StudentList.as_view()),
    url(r'^api/register/parent$', s_views.ParentRegisterView.as_view(), name='api-parent-register'),
    # url(r'^api/register/student', s_views.StudentRegisterView.as_view(), name='api-student-register'),
]
