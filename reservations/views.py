"""
Reservation API Views
Provides REST API endpoints for Reservation model
"""
from rest_framework import viewsets
from .models import Reservation
from .serializers import ReservationSerializer
from .permissions import IsAdminOrOwner
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone


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
    permission_classes = [IsAdminOrOwner]

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

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """
        Activate a reservation (status: confirmed -> active).
        Only staff can activate.
        """
        reservation = self.get_object()

        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can activate reservations."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if reservation.status != 'confirmed':
            return Response(
                {"detail": "Only confirmed reservations can be activated."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation.status = 'active'
        reservation.save()

        serializer = self.get_serializer(reservation)
        return Response(
            {"message": "Reservation activated successfully.", "reservation": serializer.data},
            status=status.HTTP_200_OK,
        )
        
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Complete a reservation (status: active -> completed).
        Only staff can complete.
        """
        reservation = self.get_object()
        
        if not request.user.is_staff:
            return Response(
                {"detail": "Only staff can complete reservations."},
                status=status.HTTP_403_FORBIDDEN,
            )
            
        if reservation.status != 'active':
            return Response(
                {"detail": "Only active reservations can be completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        reservation.status = 'completed'
        reservation.save() 
        
        serializer = self.get_serializer(reservation)
        return Response(
            {"message": "Reservation completed successfully.", "reservation": serializer.data},
            status=status.HTTP_200_OK,
        )
           
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancel a reservation (status: pending/confirmed -> cancelled).
        Staff or owner can cancel.
        """
        reservation = self.get_object()
        
        if not (request.user.is_staff or reservation.user == request.user):
            return Response(
                {"detail": "You do not have permission to cancel this reservation."},
                status=status.HTTP_403_FORBIDDEN,
            ) 
            
        if not reservation.can_be_cancelled():
            return Response(
                {"detail": "Only pending or confirmed reservations can be cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )
           
        # Calculate fee and store cancellation info
        fee = reservation.get_cancellation_fee()
        reservation.cancellation_fee = fee
        reservation.cancellation_date = timezone.now()
        reservation.cancelled_by = request.user
        reservation.cancellation_reason = request.data.get("reason", "")
           
        reservation.status = 'cancelled'
        reservation.save()
        
        serializer = self.get_serializer(reservation)
        return Response(
            {"message": "Reservation cancelled successfully.", "reservation": serializer.data},
            status=status.HTTP_200_OK,
        )
        
    @action(detail=True, methods=['get'])
    def cancellation_policy(self, request, pk=None):
        """
        Show cancellation policy for a reservation.
        """
        reservation = self.get_object()

        policy = {
            "cancellable_statuses": ["pending", "confirmed"],
            "not_cancellable_statuses": ["active", "completed", "cancelled"],
            "rules": [
                "48+ hours before start: no fee",
                "24-48 hours before start: 50% fee",
                "Less than 24 hours before start: 100% fee",
            ],
        }

        return Response(
            {"reservation_id": reservation.id, "policy": policy},
            status=status.HTTP_200_OK,
        )
        
    @action(detail=True, methods=['get'])
    def cancellation_fee(self, request, pk=None):
        """
        Preview cancellation fee for a reservation.
        """
        reservation = self.get_object()

        fee = reservation.get_cancellation_fee()
        if fee is None:
            return Response(
                {"detail": "This reservation cannot be cancelled or fee cannot be calculated."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        return Response(
            {"reservation_id": reservation.id, "cancellation_fee": fee},
            status=status.HTTP_200_OK,
        )