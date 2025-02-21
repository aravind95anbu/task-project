from django.contrib.auth.models import AbstractUser
from django.db import models

class Right(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Role(models.Model):
    name = models.CharField(max_length=255)
    rights = models.ManyToManyField(Right)

    def __str__(self):
        return self.name

class Member(AbstractUser):
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username

