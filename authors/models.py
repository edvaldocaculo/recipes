
from django.contrib.auth import get_user_model
from django.db import models  # noqa: E501

User = get_user_model()


class Profile(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE,)
    bio = models.TextField(default='', blank=True,)

    def __str__(self):
        return self.bio
