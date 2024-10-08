from rest_framework import serializers
from finance.models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'user_id', 
            'balance',
        ]
