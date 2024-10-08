from django.urls import path
from django.urls import include
from users.views import SignUpViewSet
from users.views import UpdateInformationViewSet
from users.views import UpdateProfileView
from users.views import ChangePasswordView

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'sign_up', SignUpViewSet, basename='sign_up')
router.register(r'update_and_finance', UpdateInformationViewSet, basename='update')

urlpatterns = [
    path('', include(router.urls)),
    path('finance/', include('finance.urls')),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
]
