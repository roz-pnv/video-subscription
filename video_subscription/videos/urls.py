from django.urls import path, include
from rest_framework.routers import DefaultRouter
from videos.views import VideoViewSet
from videos.views import ActorViewSet
from videos.views import DirectorViewSet
from videos.views import LanguageViewSet 
from videos.views import CategoryViewSet
from videos.views import SubscriptionViewSet
from videos.views import HistoryViewSet


router = DefaultRouter()
router.register(r'video', VideoViewSet, basename='video')
router.register(r'actor', ActorViewSet, basename='actor')
router.register(r'director', DirectorViewSet, basename='director')
router.register(r'language', LanguageViewSet, basename='language')
router.register(r'category', CategoryViewSet, basename='category')
router.register(r'subscription', SubscriptionViewSet, basename='subscription')
router.register(r'history', HistoryViewSet, basename='history')


urlpatterns = [
    path('', include(router.urls)),
    path('video/1/room/', include('public_chat.urls')), 
]
