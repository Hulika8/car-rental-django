"""
Car API Views
Provides REST API endpoints for Car model
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Car
from .serializers import CarSerializer

class CarViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Car model
    
    Provides:
        - GET /api/cars/ → List all cars
        - POST /api/cars/ → Create new car
        - GET /api/cars/{id}/ → Retrieve car details
        - PUT /api/cars/{id}/ → Update car
        - DELETE /api/cars/{id}/ → Delete car
    
    Permissions:
        - Read: Anyone (authenticated or not)
        - Write: Only authenticated users
    """
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
