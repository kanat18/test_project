from django.db import models
from django.contrib.auth.models import User



class UserMessages(models.Model):
    token = models.TextField()
    text = models.TextField()
    date = models.DateTimeField(auto_now_add=True)








