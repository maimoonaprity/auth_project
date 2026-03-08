
from rest_framework import serializers
from .models import User, Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from django.utils import timezone

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    access_duration= serializers.DurationField()
    class Meta:
        model = User
        fields = ['username', 'password','access_duration']
    
    def create(self, validated_data):
    
        user = User(
            username=validated_data['username'],
            access_duration=validated_data['access_duration']
        )
        user.set_password(validated_data['password']) 
        
        user.save()
        return user    




class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
   def validate(self, attrs):
    data = super().validate(attrs)

    user = self.user

    # Check if access duration has expired

    access_end = user.created_at + user.access_duration

    now = timezone.now()

    if now > access_end:

        raise serializers.ValidationError("Access expired. You cannot login anymore.")

    # Add remaining validity time to response if you want

    remaining_seconds = (access_end - now).total_seconds()

    data['remaining_validity_seconds'] = remaining_seconds

    return data

class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username', read_only=True)
    class Meta:
        model = Profile
        fields = ['username','age', 'address', 'dob']


