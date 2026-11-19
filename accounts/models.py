from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        BORROWER = 'borrower', 'Borrower'
        LENDER = 'lender', 'Lender'

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=8, choices=Role.choices, default=Role.BORROWER)

    def __str__(self):
        return self.email
   