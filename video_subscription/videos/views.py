from django.shortcuts import render
from videos.models import Actor
from videos.models import Director
from videos.models import Language
from videos.models import Category
from videos.models import Video
from videos.serializers import ActorSerializer
from videos.serializers import DirectorSerializer
from videos.serializers import LanguageSerializer
from videos.serializers import CategorySerializer
from videos.serializers import VideoSerializer
from videos.filters import VideoFilter
from rest_framework.permissions import AllowAny
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff
    from rest_framework import permissions

    # def has_object_permission(self, request, view, obj):
    #     if request.user and request.user.is_staff:
    #         return True

    #     if request.method == 'GET' and not obj.is_subscription_needed:
    #         return True

    #     return False



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

