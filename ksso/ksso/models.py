# -*- coding:utf-8 -*-

from django.db import models


class PortalInfo(models.Model):
    class Meta:
        app_label = 'ksso'

    uid = models.CharField(max_length=128, null=True, blank=True)
    # TODO insert additional data fields from portal sso xml

    user = models.OneToOneField('auth.User', primary_key=True, related_name='portal_info')

    @classmethod
    def create(cls, uid, user):
        return cls(uid=uid, user=user)


class PortalData(models.Model):
    class Meta:
        app_label = 'ksso'

    data = models.TextField()