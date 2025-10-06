from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cars.models import Car
from datetime import date

class Reservation(models.Model):
    # User relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name="User")
    
    # Car relationship
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reservations', verbose_name="Vehicle")
    
    # Reservation dates
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    
    # Pricing
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Daily Rate (USD)")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Total Amount (USD)")
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.car.brand} {self.car.model} ({self.start_date} to {self.end_date})"
    
    # Business logic methods
    def get_duration_days(self):
     return (self.end_date - self.start_date).days
    
    def get_total_amount(self):
        return self.daily_rate * self.get_duration_days()
    
    def get_status_display(self):
        return dict(self.STATUS_CHOICES).get(self.status, 'Unknown')
    
    def can_be_cancelled(self):
        return self.status in ['pending', 'confirmed']
    
    def is_active(self):
        return self.status == 'active'
    
    def is_completed(self):
        return self.status == 'completed'
    
    def is_cancelled(self):
        return self.status == 'cancelled'
    
    # Model validation
    def clean(self):
        # Basic field validations
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")
        if self.start_date < date.today():
            raise ValidationError("Start date cannot be in the past")
        if self.end_date < date.today():
            raise ValidationError("End date cannot be in the past")
        if self.daily_rate <= 0:
            raise ValidationError("Daily rate must be greater than 0")
        
        # Business logic validations
        if not self.user.is_active:
            raise ValidationError("User is not active")
        if not self.car.can_be_rented():
            raise ValidationError("Car is not available for rental")
    
    def save(self, *args, **kwargs):
        self.clean()
        if not self.total_amount:
            self.total_amount = self.get_total_amount()
        super().save(*args, **kwargs)