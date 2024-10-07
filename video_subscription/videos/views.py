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
from videos.filters import VideoFilter
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from rest_framework.response import Response
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

class DirectorViewSet(viewsets.ModelViewSet):
    queryset = Director.objects.all()
    serializer_class = DirectorSerializer
    permission_classes = [IsAdminOrReadOnly]

class LanguageViewSet(viewsets.ModelViewSet):
    queryset = Language.objects.all()
    serializer_class = LanguageSerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

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

        if user.is_authenticated:
           
            History.objects.create(
                user_id=user,
                video_id=instance,
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class SubscriptionViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user_id=self.request.user)
    

class HistoryViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = HistorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return History.objects.filter(user_id=self.request.user)
    