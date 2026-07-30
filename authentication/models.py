from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class UserType(models.TextChoices):
        QUIZMAKER = 'quizmaker', 'Create Quiz and Test Them'
        PERTICIPANT = 'perticipant', 'Perticipant'
    user_type = models.CharField(max_length=20, choices=UserType, default=UserType.PERTICIPANT)