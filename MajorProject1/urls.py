"""MajorProject1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin

from InfoSystem.admin_views import upload_info, display_links, upload_results

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('InfoSystem.urls')),
    url(r'^api/', include('djoser.urls.authtoken', namespace='djoser')),
    url(r'^admin/links/$', display_links, name='links'),
    url(r'^admin/info/$', upload_info, name='upload_info'),
    url(r'^admin/results/$', upload_results, name='upload_results'),
]
