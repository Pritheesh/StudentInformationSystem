from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from InfoSystem import views

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login_user, name='login')
]
