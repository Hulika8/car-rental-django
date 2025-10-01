from django.db import models
from django.core.exceptions import ValidationError

class Car(models.Model):
    """
    Car model - Vehicle rental system for global companies
    
    Global Best Practices:
    - English field names and verbose names
    - International standards
    - Professional terminology
    - Scalable for multinational operations
    """
    
    # Vehicle information
    brand = models.CharField(max_length=100, verbose_name="Brand")
    model = models.CharField(max_length=100, verbose_name="Model")
    year = models.IntegerField(verbose_name="Year")
    color = models.CharField(max_length=50, verbose_name="Color")
    
    # Pricing information
    daily_price = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Daily Rate"
    )
    
    # Vehicle status
    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_rented = models.BooleanField(default=False, verbose_name="Rented")
    is_damaged = models.BooleanField(default=False, verbose_name="Damaged")
    is_maintenance = models.BooleanField(default=False, verbose_name="In Maintenance")
    
    # Vehicle image
    image = models.ImageField(
        upload_to='vehicles/', 
        blank=True, 
        null=True, 
        verbose_name="Vehicle Image"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True, 
        verbose_name="Created At"
    )
    updated_at = models.DateTimeField(
        auto_now=True, 
        verbose_name="Updated At"
    )
    
    class Meta:
        verbose_name = "Vehicle"
        verbose_name_plural = "Vehicles"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"
    
    # BUSINESS LOGIC METHODS
    def can_be_rented(self):
        """
        Check if vehicle is available for rental
        
        Returns:
            bool: True if vehicle can be rented
        """
        return (self.is_active and 
                not self.is_rented and 
                not self.is_damaged and 
                not self.is_maintenance)
    
    def get_status(self):
        """
        Get vehicle status
        
        Returns:
            str: Vehicle status
        """
        if self.is_maintenance:
            return "In Maintenance"
        elif self.is_damaged:
            return "Damaged"
        elif self.is_rented:
            return "Rented"
        else:
            return "Available"
    
    def get_rental_status(self):
        """
        Get detailed rental status for API responses
        
        Returns:
            str: Detailed rental status
        """
        if not self.can_be_rented():
            if self.is_maintenance:
                return "In Maintenance - Not Available"
            elif self.is_damaged:
                return "Damaged - Not Available"
            elif self.is_rented:
                return "Rented - Not Available"
            else:
                return "Not Available"
        else:
            return "Available for Rental"
    
    # MODEL VALIDATION (Security)
    def clean(self):
        """
        Model validation - Ensure data integrity
        """
        if self.is_rented and self.is_active:
            raise ValidationError("Rented vehicle cannot be active!")
        
        if self.is_maintenance and self.is_active:
            raise ValidationError("Vehicle in maintenance cannot be active!")
        
        if self.is_damaged and self.is_active:
            raise ValidationError("Damaged vehicle cannot be active!")
        
        if self.year < 1900 or self.year > 2030:
            raise ValidationError("Invalid year! Must be between 1900-2030")
        
        if self.daily_price <= 0:
            raise ValidationError("Daily rate must be greater than 0!")
    
    def save(self, *args, **kwargs):
        """
        Save with validation
        """
        self.clean()
        super().save(*args, **kwargs)