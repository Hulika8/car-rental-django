from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'phone', 'address', 'city', 'state', 'zip_code', 'license_number', 'date_of_birth', 'is_verified', 'is_active']

class UserMeSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(source = 'userprofile.phone')
    address = serializers.CharField(source = 'userprofile.address')
    city = serializers.CharField(source = 'userprofile.city')
    state = serializers.CharField(source = 'userprofile.state')
    zip_code = serializers.CharField(source = 'userprofile.zip_code')
    license_number = serializers.CharField(source = 'userprofile.license_number')
    date_of_birth = serializers.DateField(source = 'userprofile.date_of_birth')
    is_verified = serializers.BooleanField(source = 'userprofile.is_verified')
    is_active = serializers.BooleanField(source = 'userprofile.is_active')
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'phone', 'address', 'city', 'state', 'zip_code', 'license_number', 'date_of_birth', 'is_verified', 'is_active']