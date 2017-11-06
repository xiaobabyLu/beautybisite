from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^register/',views.register,name='register'),
    url(r'^add_user/', views.add_user, name='add_user'),
    url(r'^userlist/', views.userlist, name='userlist'),
    url(r'^edit_user/(\d+)/$', views.edit_user, name='edit_user'),

    url(r'^del_user/(\d+)/$', views.del_user, name='del_user'),
    url(r'^testcharts/', views.testcharts, name='testcharts'),
]