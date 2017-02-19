from django.db import models


class PortalInfo(models.Model):
    user = models.OneToOneField(
        'auth.User', primary_key=True, related_name='portal_info')
    kaist_uid = models.CharField(max_length=128, unique=True)

    # TODO: Insert additional data fields from portal sso xml.
    # Field name should be same with xml field name.

    def __str__(self):
        # return self.ku_kname
        return self.user.username

    @classmethod
    def create(cls, user, kaist_uid):
        return cls(user=user, kaist_uid=kaist_uid)
