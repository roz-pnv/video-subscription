from rest_framework import viewsets
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from finance.models import Wallet 
from finance.models import Transaction
from finance.serializers import WalletSerializer
from finance.serializers import TransactionSerializer
from finance.serializers import DepositTransactionSerializer 
from finance.serializers import VerificationSerializer
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
import random

class WalletViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(user_id=self.request.user)

    @action(detail=True, methods=['get'])
    def deposit(self, request, pk=None):
        data = {
            'inventory_increase': request.build_absolute_uri(reverse('amount-request')),
        }
        return Response(data)
    

class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(wallet_id__user_id=self.request.user)


class AmountRequestAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepositTransactionSerializer

    def post(self, request, *args, **kwargs):
        serializer = DepositTransactionSerializer(data=request.data)
        if serializer.is_valid():
            wallet = Wallet.objects.get(user_id=request.user)
            transaction = Transaction.objects.create(
                wallet_id=wallet,
                type=Transaction.TransactionTypeChoices.DEPOSIT,
                amount=serializer.validated_data['amount']
            )

            verification_code = random.randint(100000, 999999)
            request.session['verification_code'] = verification_code

            send_mail(
                'Verification code',
                f'Your verification code is: {verification_code}',
                settings.EMAIL_HOST_USER,
                [request.user.email],
                fail_silently=False
            )
            
            return Response(
                {
                    'message': 'Verification code sent.', 
                    'payment_gateway_url': request.build_absolute_uri(reverse('payment-gateway', kwargs={'transaction_id': transaction.id})),
                }, 
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PaymentGatewayAPIView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepositTransactionSerializer

    def post(self, request, transaction_id, *args, **kwargs):
        transaction = get_object_or_404(Transaction, id=transaction_id)
        wallet = get_object_or_404(Wallet, user_id=request.user)
        serializer = VerificationSerializer(data=request.data)

        if serializer.is_valid():
            code = serializer.validated_data['verification_code']
            verification_code = request.session.get('verification_code')

            if verification_code == int(code):
                wallet.balance += transaction.amount
                wallet.save()
                transaction.status = Transaction.StatusChoices.SUCCESS
            else:
                transaction.status = Transaction.StatusChoices.FAILED

            transaction.save()
            return Response(
                {
                    'message': 'Transaction completed', 
                    'transaction_id': transaction.id, 
                    'status': transaction.status
                }, 
                status=status.HTTP_200_OK
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
