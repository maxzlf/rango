from django.conf.urls import re_path
from . import views, tool_views, const_views


urlpatterns = [
    re_path('^v1.0/ping$', const_views.PingView.as_view()),
    re_path('^v1.0/example$', views.ExampleView.as_view()),
    re_path('^v1.0/classes$', views.ClassesView.as_view()),
    re_path('^v1.0/classes/(?P<class_id>[0-9a-zA-Z-_]+)$',
            views.ClassesView.as_view()),
    re_path('^v1.0/classes/(?P<class_id>[0-9a-zA-Z-_]+)/students$',
            views.StudentsView.as_view()),
    re_path('^v1.0/students/(?P<student_id>[0-9a-zA-Z-_]+)$',
            views.StudentView.as_view()),
    re_path('^v1.0/constants$', const_views.ConstantsView.as_view()),
    re_path('^v1.0/constants/(?P<key>[0-9a-zA-Z-_]+)$',
            const_views.ConstantView.as_view()),
    re_path('^v1.0/users$', views.UsersView.as_view()),
    re_path('^v1.0/login$', views.LoginView.as_view()),
    re_path('^tools/v1.0/hmac$', tool_views.HmacView.as_view()),
]
