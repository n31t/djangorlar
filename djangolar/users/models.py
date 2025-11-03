from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUserAbstractUser(AbstractUser):
    phone_number = models.CharField(
        blank=True,
        null=True,
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
    )
    bio = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = "User (AbstractUser approach)"
        verbose_name_plural = "Users (AbstractUser approach)"
        db_table = 'custom_user_abstract_user'

    def __str__(self):
        return f"{self.username} ({self.email})"
