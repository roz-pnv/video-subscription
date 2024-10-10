from django.shortcuts import render
from videos.models import Actor
from videos.models import Director
from videos.models import Language
from videos.models import Category
from videos.models import Video
from videos.models import Subscription
from videos.models import History
from videos.serializers import ActorSerializer
from videos.serializers import DirectorSerializer
from videos.serializers import LanguageSerializer
from videos.serializers import CategorySerializer
from videos.serializers import VideoSerializer
from videos.serializers import SubscriptionSerializer
from videos.serializers import HistorySerializer
from videos.serializers import RenewSubscriptionSerializer
from finance.models import Wallet
from finance.models import Transaction
from videos.filters import VideoFilter
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    from rest_framework import permissions


class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']


class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name']


class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
    ]
    filter_backends = [SearchFilter]
    search_fields = ['name']


class VideoViewSet(viewsets.ModelViewSet):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [
        DjangoFilterBackend, 
        filters.SearchFilter,
    ]
    filterset_class = VideoFilter
    search_fields = ['name', 'description']

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user
        serializer = self.get_serializer(instance)

        video_url = f'http://127.0.0.1:8000/chatroom/{instance.name}/'

        if user.is_authenticated and video_url != 'You need to purchase a subscription to view the video.':
           
            History.objects.create(
                user_id=user,
                video_id=instance,
            )

        return Response(serializer.data)


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user_id=self.request.user)
    
    @action(detail=True, methods=['post', 'get'])
    def renew(self, request, pk=None):
        subscription = self.get_object()
        serializer = RenewSubscriptionSerializer(data=request.data)

        wallet = Wallet.objects.get(user_id=subscription.user_id)
        
        subscription_prices = {
            'One_month': 100000.00,
            'Quarterly': 250000.00,
            'Six_month': 450000.00,
            'One_year': 800000.00,
        }

        subscription_price = subscription_prices.get(subscription.type, 0.00)

        if wallet.balance >= subscription_price:
            if serializer.is_valid():
                serializer.update(subscription, serializer.validated_data)
                subscription.save()

                wallet.balance -= subscription_price
                wallet.save()

                transaction = Transaction.objects.create(
                    wallet_id=wallet,
                    status=Transaction.StatusChoices.SUCCESS,
                    type=Transaction.TransactionTypeChoices.WITHDRAWAL,
                    amount=subscription_price
                )
                return Response(
                    {
                        'status': 'subscription renewed', 
                        'new_balance': wallet.balance,
                        'transaction_code': transaction.id,
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            return Response({'status': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)

        
    @action(detail=True, methods=['post', 'get'])
    def cancel(self, request, pk=None):
        subscription = self.get_object()
        subscription.cancel()
        return Response({'status': 'subscription cancelled'}, status=status.HTTP_200_OK)


class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user_id=self.request.user)
    