from rest_framework import serializers
from finance.models import Wallet
from finance.models import Transaction

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'user_id', 
            'balance',
        ]


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            'wallet', 
            'subscription', 
            'status', 
            'type', 
            'amount',
        ] 
