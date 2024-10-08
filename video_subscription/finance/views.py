from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import Wallet, Transaction
from .serializers import WalletSerializer, TransactionSerializer

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user_id=self.request.user)

    @action(detail=True, methods=['post'])
    def deposit(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get('amount')

        transaction = Transaction.objects.create(
            wallet_id=wallet,
            type=Transaction.TransactionTypeChoices.DEPOSIT,
            status=Transaction.StatusChoices.PENDING,
            amount=amount,
        )
        transaction.status = Transaction.StatusChoices.SUCCESS
        transaction.save()

        wallet.balance += int(amount)
        wallet.save()

        return Response({'status': 'Balance updated', 'new_balance': wallet.balance})


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(wallet_id__user_id=self.request.user)

