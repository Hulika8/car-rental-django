from django.db import models
from django.core.exceptions import ValidationError

class Car(models.Model):
        
    # Vehicle information
    brand = models.CharField(max_length=100, verbose_name="Brand")
    model = models.CharField(max_length=100, verbose_name="Model")
    year = models.IntegerField(verbose_name="Year")
    color = models.CharField(max_length=50, verbose_name="Color")
    
    # Pricing information
    daily_rate = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        verbose_name="Daily Rate (USD)"
    )
    
    # Vehicle status
    in_fleet = models.BooleanField(default=True, verbose_name="In Fleet")
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
        return (self.in_fleet and 
                not self.is_rented and 
                not self.is_damaged and 
                not self.is_maintenance)
    
    def get_status(self):
        if self.is_maintenance:
            return "In Maintenance"
        elif self.is_damaged:
            return "Damaged"
        elif self.is_rented:
            return "Rented"
        else:
            return "Available"
    
    def get_rental_status(self):
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
        
    def get_daily_rate_display(self):
        return f"${self.daily_rate:.2f}"
    
    # MODEL VALIDATION (Security)
    def clean(self):
        """
        Model validation - Ensure data integrity
        """ 
        if self.year < 1900 or self.year > 2030:
            raise ValidationError("Invalid year! Must be between 1900-2030")
        
        if self.daily_rate <= 0:
            raise ValidationError("Daily rate must be greater than 0!")
    
    def save(self, *args, **kwargs):
        """
        Save with validation
        """
        self.clean()
        super().save(*args, **kwargs)