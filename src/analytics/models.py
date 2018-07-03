from django.db import models

# Create your models here.
from shortener.models import URL


class ClickEventManager(models.Manager):
    def create_event(self, kirrInstance):
        if isinstance(kirrInstance, URL):
            obj, created = self.get_or_create(kirr_url=kirrInstance)
            obj.count += 1
            obj.save()
            return obj.count
        return None

class ClickEvent(models.Model):
    kirr_url    = models.OneToOneField(URL)
    count       = models.IntegerField(default=0)
    updated     = models.DateTimeField(auto_now=True) 
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = ClickEventManager()

    def __str__(self):
        return "{i}".format(i=self.count)