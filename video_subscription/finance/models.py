from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from videos.models import Subscription

class Wallet(models.Model):
    user_id = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    balance = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user_id}'


class Transaction(models.Model):
    class TransactionTypeChoices(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Deposit'
        WITHDRAWAL = 'WITHDRAWAL', 'Withdrawal'

    class StatusChoices(models.TextChoices):
        SUCCESS = 'SUCCESS', 'Success'
        PENDING = 'PENDING', 'Pending'
        FAILED = 'FAILED', 'Failed'

    wallet_id = models.ForeignKey(
        Wallet, 
        on_delete=models.CASCADE,
    )
    subscription_id = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        null=True, 
        blank=True,
    )
    status = models.CharField(max_length=7, choices=StatusChoices.choices, default=StatusChoices.PENDING)
    type = models.CharField(max_length=10, choices=TransactionTypeChoices.choices)
    amount = models.PositiveIntegerField(validators=[MinValueValidator(5000)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.wallet_id}: {self.type} {self.amount} ({self.status})'
