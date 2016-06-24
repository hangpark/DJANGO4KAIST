# -*- coding:utf-8 -*-

from django.conf import settings
from django.views.generic import View, TemplateView
from django.contrib.auth import login, logout
from django.shortcuts import redirect

from kaistusc import settings


class LoginView(TemplateView):
    template_name = 'ksso/login.html'

    def dispatch(self, request, *args, **kwargs):
        from .classes import PortalController

        self.token = self.request.COOKIES.get('SATHTOKEN', False)

        if self.token:
            self.user = PortalController(self.token).retrieve_user()
            if self.user:
                login(request, self.user)

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def render_to_response(self, context, **response_kwargs):
        if self.token:
            response = redirect(settings.LOGIN_REDIRECT_URL)
            response.delete_cookie('SATHTOKEN', '/', '.kaist.ac.kr')
            return response

        return super(LoginView, self).render_to_response(context, **response_kwargs)

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        if self.token:
            context['token'] = self.token

        return context

class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect(settings.LOGIN_REDIRECT_URL)
