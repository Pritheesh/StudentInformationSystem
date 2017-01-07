from django.conf.urls import url

from InfoSystem.views import StudentListView

urlpatterns = [
    url(r'^view/$', StudentListView.as_view(), name='student-list'),
]
