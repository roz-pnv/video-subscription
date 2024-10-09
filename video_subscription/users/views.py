from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from rest_framework import viewsets
from users.serializers import SignUpSerializer
from users.serializers import ChangePasswordSerializer
from users.serializers import UpdateProfileSerializer
from rest_framework import permissions
from django.urls import reverse


class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user and (request.user.is_staff or obj == request.user)
    

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class HomeViewSet(viewsets.ViewSet):
    
    def list(self, request):
        data = {
            'auth_url': request.build_absolute_uri('/api/auth/'),
            'videos_url': request.build_absolute_uri('/api/videos/')
        }
        return Response(data)
    

class UpdateInformationViewSet(viewsets.ViewSet):
    
    def list(self, request):
        data = {
            'update_profile_url': request.build_absolute_uri(reverse('update_profile')),
            'change_password_url': request.build_absolute_uri(reverse('change_password')),
            'wallet': request.build_absolute_uri(reverse('wallet-detail', kwargs={'pk': request.user.wallet.id})),
            'transactions_history': request.build_absolute_uri(reverse('transaction-list')),
            'inventory_increase': request.build_absolute_uri(reverse('amount-request')),
        }
        return Response(data)
    

class SignUpViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    permission_classes = (
        IsAuthenticated, 
        IsOwnerOrAdmin,
    )
    serializer_class = SignUpSerializer

    def get_permissions(self):
        if self.action in ['retrieve', 'list', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        elif self.action == 'create':
            self.permission_classes = [AllowAny]
        elif self.action in ['update', 'partial_update']:
            self.permission_classes = [IsAuthenticated, IsAdminOrReadOnly]
        return super(SignUpViewSet, self).get_permissions()
    
    def get_queryset(self):
        if self.request.user.is_staff:
            return Profile.objects.all()
        return Profile.objects.filter(user=self.request.user)


class UpdateProfileView(generics.GenericAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = UpdateProfileSerializer
    throttle_classes = [
        AnonRateThrottle,
        UserRateThrottle,
    ]

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()

        return Response({'success': True})


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = (
        IsAuthenticated,
    )
    serializer_class = ChangePasswordSerializer
    queryset = User.objects.all()
