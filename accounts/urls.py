from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.views import RegisterAPIView, LoginAPIView, UserViewSet, CreateUserView
from src.custom_router import CustomRouter

router = CustomRouter()

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('token/', LoginAPIView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('accounts/me/', UserViewSet.as_view({'get': 'retrieve'}), name='accounts_me'),
    path('accounts/', UserViewSet.as_view({'get': 'list'}), name='accounts'),
    path('accounts/create/', CreateUserView.as_view(), name='accounts_create'),
] + router.urls
