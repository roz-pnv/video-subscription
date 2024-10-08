from django.urls import path, include
from rest_framework.routers import DefaultRouter
from finance.views import WalletViewSet
from finance.views import TransactionViewSet
from finance.views import AmountRequestAPIView
from finance.views import PaymentGatewayAPIView
from finance.views import WalletViewSet
from users.views import UpdateInformationViewSet

router = DefaultRouter()
router.register(r'wallets', WalletViewSet)
router.register(r'transactions', TransactionViewSet)
router.register(r'update_and_finance', UpdateInformationViewSet, basename='update')

urlpatterns = [
    path('', include(router.urls)),
    path('amount-request/', AmountRequestAPIView.as_view(), name='amount-request'),
    path('payment-gateway/<int:transaction_id>/', PaymentGatewayAPIView.as_view(), name='payment-gateway'),
]