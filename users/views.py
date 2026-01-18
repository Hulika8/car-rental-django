from django.contrib.auth.models import User
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from rest_framework.permissions import IsAuthenticated
from .serializers import UserMeSerializer
from rest_framework.permissions import IsAdminUser

class RegisterAPIView(APIView):
    def post(self, request):
        data = request.data

        required_fields = [
            'username', 'email', 'password',
            'first_name', 'last_name', 'phone',
            'address', 'city', 'state', 'zip_code',
            'license_number', 'date_of_birth'
        ]

        missing = [field for field in required_fields if not data.get(field)]
        if missing:
            return Response(
                {"error": f"Missing fields: {', '.join(missing)}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(email=email).exists():
            return Response(
                {"error": "Email already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if UserProfile.objects.filter(phone=data.get('phone')).exists():
            return Response(
                {"error": "Phone number already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if UserProfile.objects.filter(license_number=data.get('license_number')).exists():
            return Response(
                {"error": "License number already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=data.get('first_name'),
                last_name=data.get('last_name')
            )

            UserProfile.objects.create(
                user=user,
                phone=data.get('phone'),
                address=data.get('address'),
                city=data.get('city'),
                state=data.get('state'),
                zip_code=data.get('zip_code'),
                license_number=data.get('license_number'),
                date_of_birth=data.get('date_of_birth'),
                is_verified=False,
                is_active=True
            )

        return Response(
            {"message": "User created successfully"},
            status=status.HTTP_201_CREATED
        )
        
class UserMeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserMeSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class AdminOnlyAPIView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        return Response(
            {"message": "Admin access granted"},
            status=status.HTTP_200_OK
        )