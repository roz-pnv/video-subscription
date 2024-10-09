from django.urls import path, include
from django.contrib.auth import views
from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter
from users.views import HomeViewSet

router = DefaultRouter()
router.register(r'', HomeViewSet, basename='home') 

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view(template_name='rest_framework/login.html'), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/', include('users.urls')),
    path('api/videos/', include('videos.urls')),
]
