from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.db import models

alpha = RegexValidator(r'^[a-zA-Z]+$', 'Only alpha characters of length 1 or more are accepted')


class Profile(models.Model):
    name = models.TextField(validators=[alpha])

    user_id = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
