from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Profile
from .permissions import HasValidAccess, IsOwner
from .serializers import RegisterSerializer, ProfileSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.utils import timezone


class RegisterUserAPIView(APIView):
   
    def post(self, request):

        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework_simplejwt.views import TokenObtainPairView

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ProfileAPIView(APIView):

    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, HasValidAccess, IsOwner]


    def get(self, request):
        # print(f"User: {request.user}")
        # print(f"Auth Method: {request.auth}")
        serializer = RegisterSerializer(request.user)
        return Response(serializer.data)


import os
from django.http import FileResponse, Http404
from django.conf import settings

# def download_exe(request):

 

#     exe_path = os.path.join(settings.BASE_DIR, "dist", "hello.exe")
#     if os.path.exists(exe_path):
#         # The filename parameter sets the name for the downloaded file
#         return FileResponse(open(exe_path, "rb"), as_attachment=True, filename="hello.exe")
#     else:
#         raise Http404("File not found") 


class DownloadExeView(APIView):
    permission_classes = [IsAuthenticated, HasValidAccess, IsOwner]   # 🔐 Only logged-in users can download

    def get(self, request):
        exe_path = os.path.join(settings.BASE_DIR, "dist", "hello.exe")

        if os.path.exists(exe_path):
            return FileResponse(
                open(exe_path, "rb"),
                as_attachment=True,
                filename="hello.exe"
            )
        else:
            raise Http404("File not found")       

