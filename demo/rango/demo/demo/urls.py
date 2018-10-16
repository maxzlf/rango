from django.conf.urls import re_path
from . import views


urlpatterns = [
    re_path('^v1.0/ping$', views.PingView.as_view()),
    re_path('^v1.0/example$', views.ExampleView.as_view()),
]
