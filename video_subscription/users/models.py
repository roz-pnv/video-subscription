from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^0[0-9]{9}$',
                message='Invalid phone number.'
            ),
        ],
        unique=True,
    )
    is_admin = models.BooleanField(default=False)
    description = models.TextField()
    birthdate = models.DateField(null=True, blank=True)
    national_id = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'\d{10}',
                message='Invalid national ID.'
            ),
        ],
        unique=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

