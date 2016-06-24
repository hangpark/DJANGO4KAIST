# -*- coding:utf-8 -*-

from django.db import models


class PortalInfo(models.Model):
    user = models.OneToOneField('auth.User', primary_key=True, related_name='portal_info')
    kaist_uid = models.CharField(max_length=128, blank=True, unique=True)
    # TODO insert additional data fields from portal sso xml

    @classmethod
    def create(cls, user, kaist_uid):
        return cls(user=user, kaist_uid=kaist_uid)
