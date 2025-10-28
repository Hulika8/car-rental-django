"""
Reservation API Views
Provides REST API endpoints for Reservation model
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Reservation
from .serializers import ReservationSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Reservation model
    
    Provides:
        - GET /api/reservations/ → List all reservations
        - POST /api/reservations/ → Create new reservation
        - GET /api/reservations/{id}/ → Retrieve reservation details
        - PUT /api/reservations/{id}/ → Update reservation
        - DELETE /api/reservations/{id}/ → Delete reservation
    
    Permissions:
        - All operations: Only authenticated users
    """
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """
        Filter reservations based on user role
        
        Returns:
            QuerySet: All reservations for admin, user's own for regular users
        """
        user = self.request.user
        
        # Admin/Staff can see all reservations
        if user.is_staff:
            return Reservation.objects.all()
        
        # Regular users can only see their own reservations
        return Reservation.objects.filter(user=user)
    
    def perform_create(self, serializer):
        """
        Auto-assign logged-in user when creating reservation
        Admin can override by specifying user in request
        """
        if self.request.user.is_staff:
            serializer.save()
        else:
            serializer.save(user=self.request.user, status='confirmed')
