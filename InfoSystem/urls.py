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

    url(r'^register/$', views.register, name='email-register'),
    url(r'^login/$', views.login2, name='email-login'),
    url(r'^activation/', views.activate, name='email-activate'),
    url(r'^results/$', login_required(views.result_view2), name='email-result-view'),
    # url(r'^email/forgot/$', views.forgot_password, name='email-forgot'),

    url(r'^password/reset/$', auth_views.password_reset,
        {'post_reset_redirect': '/password/reset/done/'}, name='password-reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,
        {'post_reset_redirect': '/password/done/'}, name='password-reset-confirm'),
    url(r'^password/done/$', auth_views.password_reset_complete),
    # url(r'^results/$', api_views.result_view, name='result-view'),

    url(r'^$', views.login2, name='email-login'),
    url(r'^otp/login/$', views.login_view, name='login'),
    url(r'^otp/verify/(?P<id>\S+)/$', views.otp_verify, name='otp-verify'),
    url(r'^otp/register/$', views.register2, name='register'),
    url(r'^otp/token/(?P<id>\S+)/$', views.otp_token, name='token'),
    url(r'^otp/results/$', login_required(views.result_view), name='result-view'),

    url(r'^logout/$', views.logout_view, name='logout'),
]
