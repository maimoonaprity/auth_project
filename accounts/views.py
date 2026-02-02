from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, ProfileSerializer, UserListSerializer, MyTokenObtainPairSerializer
from .permissions import IsAccessValid



class ListUser(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserListSerializer(users, many= True)
        return Response(serializer.data)



class RegisterUser(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data =request.data)
        if serializer.is_valid():
            serializer.save()
            return Response( 
                   serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)
        
class ProfileView(APIView):
    permission_classes = [IsAccessValid]

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)
        return Response(serializer.data)

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
        


        


