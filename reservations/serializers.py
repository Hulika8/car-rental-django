"""
Reservation Serializers
Converts Reservation model to/from JSON format
"""
from rest_framework import serializers
from .models import Reservation
from cars.serializers import CarSerializer
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Basic User serializer
    Only show safe fields (no password!)
    """
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        
class ReservationSerializer(serializers.ModelSerializer):
    """
    Serializer for Reservation model
    
    Features:
        - Nested car details (read-only)
        - Nested user details (read-only)
        - Auto-calculated total_amount (read-only)
        - days_count: Custom calculated field
    """
    car_details = CarSerializer(source='car', read_only=True)
    user_details = UserSerializer(source='user', read_only=True)
    days_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Reservation
        fields = '__all__'
        read_only_fields = (
            'total_amount',
            'created_at',
            'updated_at',
            'cancellation_fee',
            'cancellation_date',
            'cancelled_by',
)
        
        
    def __init__(self, *args, **kwargs):
        """
        Customize serializer fields based on user role
        
        - Admin: Can see and edit all fields (including user)
        - Regular user: Cannot see/edit user field
        """
        super().__init__(*args, **kwargs)
        
        # Get request from context
        request = self.context.get('request')
        
        # If user is not admin → Hide user field from form
        if request and not request.user.is_staff:
            # Remove user field from form (user won't see dropdown)
            self.fields.pop('user', None)
             # Make status read-only for regular users (show in response, hide in form)
            if 'status' in self.fields:
                self.fields['status'].read_only = True
                
    def get_days_count(self, obj):
        """
        Calculate reservation duration in days
        
        Returns:
            int: Number of days
        """
        return obj.get_duration_days()