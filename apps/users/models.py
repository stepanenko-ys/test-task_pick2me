from django.contrib.auth.models import User
from django.db import models


class CustomUser(User):
    phone = models.CharField(max_length=13, blank=True, null=True)
