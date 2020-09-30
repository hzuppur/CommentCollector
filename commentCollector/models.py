import datetime
from django.db import models
from django.utils import timezone


class Article(models.Model):
  id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=500)
  url = models.CharField(max_length=500)
  comments = models.IntegerField()
  pub_date = models.DateTimeField('date published')

  def __str__(self):
    return self.name

  def was_published_recently(self):
    return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Comment(models.Model):
  id = models.IntegerField(primary_key=True)
  article = models.ForeignKey(Article, on_delete=models.CASCADE)
  removed = models.BooleanField(default=False)
  content = models.CharField(max_length=4000)
  subject = models.CharField(max_length=500)

  class Meta:
    unique_together = ["id"]

  def __str__(self):
    return self.content

  def set_removed(self, value):
    self.removed = value
    return self


class CommentReply(models.Model):
  comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
  content = models.CharField(max_length=4000)
  subject = models.CharField(max_length=500)

  class Meta:
    unique_together = ["comment", "content", "subject"]

  def __str__(self):
    return self.content

class SavedComment(models.Model):
  id = models.IntegerField(primary_key=True)
  article = models.CharField(max_length=1000)
  removed = models.BooleanField(default=False)
  content = models.CharField(max_length=4000)
  subject = models.CharField(max_length=500)

  class Meta:
    unique_together = ["id"]

  def __str__(self):
    return self.content

  def set_removed(self, value):
    self.removed = value
    return self
