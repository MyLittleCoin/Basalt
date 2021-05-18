import datetime

from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
# Create your models here.
class Project(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    #path_to_file = models.CharField(max_length=200)
    file = models.FileField(upload_to='projects/', default="test.zip")
    #timestamp = models.DateTimeField(auto_now_add=True, default=now)
    def __str__(self):
        return self.name
