from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import User
from django.contrib.auth.password_validation import validate_password
from datetime import timedelta

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    access_duration = serializers.FloatField(required=True, help_text="Access duration in hours")
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'access_duration']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"message" : "password does not match"})
        
        
        if attrs['access_duration'] <= 0:
            raise serializers.ValidationError({"access_duration": "time limit over"})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        access_hours = validated_data.pop('access_duration')
        
        user = User.objects.create(
            username = validated_data['username'],
            email = validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.access_duration = timedelta(hours=access_hours)
        user.save()
        return user
        
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model= User
        fields = ['id','username', 'email']

class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Standard validation (username & password)
        data = super().validate(attrs)

        user = self.user
        if not user.has_valid_access():
            return Response({"detail": "Access expired. Unauthorized."}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Return token data if valid
        return data
