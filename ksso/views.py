# -*- coding:utf-8 -*-

from django.conf import settings
from django.views.generic import TemplateView


class LoginView(TemplateView):
    template_name = 'ksso/login.html'

    def dispatch(self, request, *args, **kwargs):
        from django.contrib.auth import login
        from .classes import PortalController

        self.token = self.request.COOKIES.get('SATHTOKEN', False)

        if self.token:
            from django.shortcuts import redirect

            self.user = PortalController(self.token).retrieve_user()
            if self.user:
                login(request, self.user)

            return redirect(settings.LOGIN_REDIRECT_URL)

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    # 성공적으로 로그인하면 Portal SSO System SATH Token 삭제
    def render_to_response(self, context, **response_kwargs):
        response = super(LoginView, self).render_to_response(context, **response_kwargs)

        if self.token:
            response.delete_cookie('SATHTOKEN')

        return response

    def get_context_data(self, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)

        if self.token:
            context['token'] = self.token

        return context
