from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import Profile
from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle
from rest_framework import status
from users.serializers import SignUpSerializer
from users.serializers import ChangePasswordSerializer
from users.serializers import UpdateProfileSerializer


class SignUpView(generics.CreateAPIView):
    queryset = Profile.objects.all()
    permission_classes = (
        AllowAny,
    )
    serializer_class = SignUpSerializer


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
    