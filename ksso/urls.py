from django.conf.urls import patterns, url
from .views import LoginView, LogoutView

urlpatterns = patterns('',
    url(r'^accounts/login/$', LoginView.as_view()),
    url(r'^accounts/logout/$', LogoutView.as_view()),
)
