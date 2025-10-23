"""
Django Signals for Reservation System
Automatically update car status based on reservation changes
"""

from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from .models import Reservation


@receiver(post_save, sender=Reservation)
def update_car_status_on_save(sender, instance, created, **kwargs):
    """
    Update car rental status when reservation is saved
    
    Business Rules:
    - status = 'active' → car.is_rented = True
    - status = 'completed' or 'cancelled' → car.is_rented = False
    
    Args:
        sender: Reservation model class
        instance: The saved reservation object
        created: Boolean - True if new reservation
        **kwargs: Additional arguments
    """
    if not instance.car:
        return
    
    if instance.status == 'active':
        if not instance.car.is_rented:
            instance.car.is_rented = True
            instance.car.save(update_fields=['is_rented'])
            print(f"🚗 Car {instance.car} is now RENTED")
    
    elif instance.status in ['completed', 'cancelled']:
        if instance.car.is_rented:
            instance.car.is_rented = False
            instance.car.save(update_fields=['is_rented'])
            print(f"🚗 Car {instance.car} is now AVAILABLE")


@receiver(pre_delete, sender=Reservation)
def update_car_status_on_delete(sender, instance, **kwargs):
    """
    Make car available when reservation is deleted
    
    Args:
        sender: Reservation model class
        instance: The reservation being deleted
        **kwargs: Additional arguments
    """
    if instance.car and instance.car.is_rented:
        instance.car.is_rented = False
        instance.car.save(update_fields=['is_rented'])
        print(f"🚗 Car {instance.car} is now AVAILABLE (reservation deleted)")       
        
        
        
        
        
        
        
        
    #reservations/
    #models.py       → Database tabloları (Car, Reservation)
    #views.py        → Kullanıcı istekleri (HTTP request/response)
    #admin.py        → Admin panel ayarları
    #signals.py      → Otomatik tetiklenen işlemler ⭐
    #apps.py         → App konfigürasyonu (ayarlar)
    #urls.py         → URL routing
    #forms.py        → Form validasyonları