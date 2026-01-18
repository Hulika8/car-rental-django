from django.db import models
from django.contrib.auth.models import User as DjangoUser

class UserProfile(models.Model):
     # User relationship
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE, verbose_name="User")
    
    # Profile information
    phone = models.CharField(max_length=20, unique=True, verbose_name="Phone Number")
    address = models.TextField(verbose_name="Address")
    city = models.CharField(max_length=100, verbose_name="City")
    state = models.CharField(max_length=100, verbose_name="State")
    zip_code = models.CharField(max_length=20, verbose_name="Zip Code")
    license_number = models.CharField(max_length=50, unique=True, verbose_name="License Number")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    
    # Status
    is_verified = models.BooleanField(default=False, verbose_name="Verified")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.user.username} - {self.user.email}"
    
    # Business logic methods
    def can_make_reservations(self):
        return self.is_verified and self.is_active
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_full_address(self):
        return f"{self.address}, {self.city}, {self.state}, {self.zip_code}"
    