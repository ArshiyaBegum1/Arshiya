from django.urls import path
from django.conf.urls import url
from rest_framework.authtoken.views import obtain_auth_token
from account.api.views import (
    registration_view,
    login,
    activate,
    # ResetPasswordRequestView
)
from account.api import views

app_name = 'account'

urlpatterns = [
    path('register', registration_view, name="register"),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         activate, name='activate'),
    path('login', login),

    path('dashboard', views.DashboardView.as_view()),
    path('kyc', views.KycView.as_view()),

    path('postproject', views.Projects.as_view()),
    path('home', views.AllProjects.as_view()),

    path('category', views.Category.as_view()),
    path('categorylist', views.CategoryList.as_view()),

    # url(r'^reset_password',ResetPasswordRequestView.as_view(), name="reset_password"),

    path('userdetailkyc', views.getKYC.as_view()),
    path('getkyc', views.getKYC.as_view()),
                               
    url(r'^password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_confirm, name='password_reset_complete'),
]
