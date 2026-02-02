from django.urls import path
from .views import RegisterUser, ProfileView, ListUser
from rest_framework_simplejwt.views import TokenObtainPairView


urlpatterns = [

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', RegisterUser.as_view(), name = 'register_user'),
    path('profile/',ProfileView.as_view() , name = 'profile'),
    path('users/',ListUser.as_view(), name = 'user-list'),
  
]
