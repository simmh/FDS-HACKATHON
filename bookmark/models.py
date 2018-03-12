from django.db import models
# from taggit.managers import TaggableManager

# Create your models here.

class bookmark(models.Model):
  url = models.URLField()
  domain = models.URLField(blank=True)
  title = models.CharField(max_length=80, blank=True)
  description = models.CharField(max_length=500, blank=True)
  pavicon = models.TextField()
  img = models.TextField()
  star = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)


