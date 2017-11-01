from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^register/',views.register,name='register'),
    url(r'^add_user/', views.add_user, name='add_user'),
    url(r'^userlist/', views.userlist, name='userlist'),
    url(r'^userinfo/(\d+)/$', views.userInfo, name='userinfo'),
]