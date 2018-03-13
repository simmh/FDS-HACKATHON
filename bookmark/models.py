from django.db import models
# from taggit.managers import TaggableManager

# Create your models here.

class Bookmark(models.Model):
  url = models.URLField()
  domain = models.URLField(blank=True)
  title = models.CharField(max_length=80, blank=True)
  description = models.CharField(max_length=500, blank=True)
  favicon = models.TextField(null=True, blank=True)
  image = models.TextField(null=True, blank=True)
  star = models.BooleanField(default=False)
  created = models.DateTimeField(auto_now_add=True)

  def __str__(self):
        return "%s %s %s %s" % (self.id, self.url, self.title[:10], self.description[:20])

