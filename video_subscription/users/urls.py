from django.urls import path
from users.views import SignUpView
from users.views import UpdateProfileView
from users.views import ChangePasswordView

from rest_framework_simplejwt.views import TokenVerifyView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('sign_up/', SignUpView.as_view(), name='sign_up'),
    path('update_profile/', UpdateProfileView.as_view(), name='update_profile'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='change_password'),
]
