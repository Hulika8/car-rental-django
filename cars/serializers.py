"""
Car Serializers
Converts Car model to/from JSON format
"""
from rest_framework import serializers
from .models import Car

class CarSerializer(serializers.ModelSerializer):
    """
    Serializer for Car model
    
    Fields:
        - All fields from Car model
        - read_only: created_at, updated_at (user cannot modify)
        - rental_status: Custom method field (can_be_rented status)
    """
    rental_status = serializers.SerializerMethodField()
    
    class Meta:
        model = Car
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')
        
    def get_rental_status(self, obj):
        """
        Custom field: Return car's rental availability status
        
        Returns:
            dict: Status details (available, reason)
        """
        return {
            'available': obj.can_be_rented(),
            'status': obj.get_rental_status()
        }   