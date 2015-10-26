from django.db import models
from django.contrib.auth.models import User
from django.utils.encoding import smart_unicode


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    dateofbirth = models.DateField()
    height = models.CharField(max_length=200)
    weight = models.CharField(max_length=200)
    IDNum = models.CharField(max_length=200)
    Residence = models.CharField(max_length=200)
    PhoneNum = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self):
        return smart_unicode(self.IDNum)