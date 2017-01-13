from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from InfoSystem import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login'),
    url(r'^$', views.login_user, name='login'),
    url(r'^accounts/login/$', views.login_user, name='login'),
    url(r'^results/$', views.result_view, name='result-view'),
    url(r'^logout/$', views.logout_view, name='logout'),
]
