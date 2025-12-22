from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import CustomUserManager
import random


# Create your models here.


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(unique=True)

    email_verification_code = models.CharField(
        max_length=6,
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def generate_verification_code(self):
        self.email_verification_code = str(random.randint(100000, 999999))
        self.save(update_fields=['email_verification_code'])


    def __str__(self):
        return self.email





