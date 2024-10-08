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
            'wallet_id', 
            'subscription_id', 
            'status', 
            'type', 
            'amount',
        ] 


class DepositTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['amount']


class VerificationSerializer(serializers.Serializer):
    verification_code = serializers.CharField(max_length=6)
