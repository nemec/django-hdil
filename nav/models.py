from django.db import models

class NewsSnippet(models.Model):
  title = models.CharField(max_length=50)
  data = models.TextField()
  pub_date = models.DateTimeField("date published")

  def __unicode__(self):
    return self.data
