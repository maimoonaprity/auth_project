from django.urls import path
from .views import RegisterUserAPIView , ProfileAPIView , CustomTokenObtainPairView, DownloadExeView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

urlpatterns = [
    
     path('login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUserAPIView.as_view(), name='register'),
    path('profile/', ProfileAPIView.as_view(), name= 'profile'),
    path('downloadexe/', DownloadExeView.as_view(), name='download-exe'),
    
    
]
