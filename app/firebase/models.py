from django.contrib.auth.models import User
from django.db import models


class Firebase(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    uid = models.TextField(unique=True)
