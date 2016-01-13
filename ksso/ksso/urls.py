from django.conf.urls import patterns, include, url
from .views import LoginView

urlpatterns = patterns('',
    url(r'^accounts/login/$', LoginView.as_view()),
)