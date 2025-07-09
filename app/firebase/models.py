from django.contrib.auth.models import User
from django.db import models


class FirebaseUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    uid = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return f"{self.user} → {self.uid}"
