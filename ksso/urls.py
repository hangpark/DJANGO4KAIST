from django.conf.urls import patterns, url
from .views import LoginView

urlpatterns = patterns('',
    url(r'^accounts/login/$', LoginView.as_view()),
)
