from django.conf.urls import re_path
from . import views


urlpatterns = [
    re_path('^v1.0/ping$', views.PingView.as_view()),
    re_path('^v1.0/example$', views.ExampleView.as_view()),
    re_path('^v1.0/students$', views.StudentsView.as_view()),
    re_path('^v1.0/students/(?P<student_id>[0-9a-zA-Z-_]+)$',
            views.StudentView.as_view()),
    re_path('^v1.0/constants$', views.ConstantsView.as_view()),
    re_path('^v1.0/constants/(?P<key>[0-9a-zA-Z-_]+)$',
            views.ConstantView.as_view()),
    re_path('^v1.0/login$', views.LoginView.as_view()),
]
