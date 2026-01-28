from datetime import date, datetime, time
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from cars.models import Car

class Reservation(models.Model):
    """
    Reservation model for car rentals
    
    TODO (Week 3 - Celery Automation):
    ═══════════════════════════════════════════════════════════════
    [ ] Add payment_deadline field (DateTimeField)
        - Auto-set to created_at + 30 minutes for pending reservations
        - Example: payment_deadline = models.DateTimeField(null=True, blank=True)
    
    [ ] Implement Celery periodic task: cleanup_expired_pending_reservations()
        - Runs every 5 minutes
        - Find: status='pending' AND created_at < (now - 30min)
        - Action: Auto-cancel + set cancellation_reason='Payment timeout'
        - Signal will auto-update: car.is_rented = False
    
    [ ] Add email notification: "Payment timeout - Reservation cancelled"
    
    [ ] Business Logic:
        - Pending → Confirmed (ödeme yapıldı) → Active → Completed ✅
        - Pending → Auto-cancelled (30min timeout) ❌
    
    Real-world example: Hertz/Enterprise 15-30min payment window
    ═══════════════════════════════════════════════════════════════
    
    TODO (Week 3-4 - Payment Integration & Advanced Workflow):
    ═══════════════════════════════════════════════════════════════
    [ ] Advanced Status Workflow:
        - Add: 'partially_paid' (deposit received)
        - Add: 'ready_for_pickup' (start date arrived)
        - Add: 'overdue' (late return)
        - Add: 'refunded' (refund completed)
    
    [ ] Payment Tracking Fields:
        - payment_status: ['unpaid', 'partial', 'paid', 'refunded']
        - deposit_amount: Kapora miktarı
        - remaining_amount: Kalan ödeme
        - payment_method: ['credit_card', 'cash', 'bank_transfer']
        - stripe_payment_id: Stripe transaction ID
        - paid_at: Ödeme tarihi
    
    [ ] Workflow Scenarios:
        ADMIN (Call Center):
        1. Create → status='pending' (bilgiler alındı)
        2. Ödeme al → status='confirmed' (manuel değiştir)
        
        CUSTOMER (API - Week 3):
        1. Create → status='pending' (ödeme bekliyor)
        2. Pay → status='confirmed' (Stripe webhook)
        3. Deposit → status='partially_paid' (kapora)
    
    Real-world: Hertz 20% deposit, Enterprise full payment option
    ═══════════════════════════════════════════════════════════════
    """
    # User relationship
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations', verbose_name="User")
    
    # Car relationship
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='reservations', verbose_name="Vehicle")
    
    # Reservation dates
    start_date = models.DateField(verbose_name="Start Date")
    end_date = models.DateField(verbose_name="End Date")
    
    # Pricing
    daily_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Daily Rate (USD)")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name="Total Amount (USD)")
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    
    # Cancellation info
    cancellation_fee = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    cancellation_date = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    cancelled_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
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
    
    # BUSINESS LOGIC: Date conflict check
    
    def check_date_conflict(self):
        """
        Check if there's any date conflict with existing reservations
        Same car cannot be rented for overlapping dates
        """
        # Find all reservations for the same car
        overlapping = Reservation.objects.filter(
            car=self.car,
            status__in=['pending', 'confirmed', 'active']
        ).exclude(pk=self.pk)  # Exclude current reservation (for updates)
        
        # Check each reservation for date overlap
        for reservation in overlapping:
            # Date overlap logic:
            # - New start date is before existing end date AND
            # - New end date is after existing start date
            if (self.start_date <= reservation.end_date and 
                self.end_date >= reservation.start_date):
                raise ValidationError(
                    f"This car is already reserved from {reservation.start_date} to {reservation.end_date}"
                )
    
    
    # Model validation
    def clean(self):
        # Basic field validations
        if self.start_date >= self.end_date:
            raise ValidationError("Start date must be before end date")
        if self.daily_rate is not None and self.daily_rate <= 0:
            raise ValidationError("Daily rate must be greater than 0")
        
        # Date validations (only for new reservations)
        if not self.pk:  # new reservation
            if self.start_date < date.today():
                raise ValidationError("Start date cannot be in the past")
            if self.end_date < date.today():
                raise ValidationError("End date cannot be in the past")
        
        # Business logic validations
        if not self.user.is_active:
            raise ValidationError("User is not active")
        
        # USER PROFILE CHECK 
        try:
            profile = self.user.userprofile
        except:
            raise ValidationError(
                f"User '{self.user.username}' does not have a profile!")
        
        if not profile.can_make_reservations():
            raise ValidationError(
                f"User '{self.user.username}' cannot make reservations. "
                f"Verified: {profile.is_verified}, Active: {profile.is_active}"
            )
        
        # CAR OPERATIONAL CHECK (Only for new reservations)
        # Note: is_rented is managed by date conflicts, not here!
        if not self.pk:
            # Check if car is in operational state
            if not self.car.in_fleet:
                raise ValidationError("Car is not in fleet!")
            if self.car.is_damaged:
                raise ValidationError("Car is damaged and cannot be rented!")
            if self.car.is_maintenance:
                raise ValidationError("Car is under maintenance and cannot be rented!")
        
        # Check for date conflicts (same car, overlapping dates)
        self.check_date_conflict()
    
    def save(self, *args, **kwargs):
        self.clean()
        if not self.total_amount:
            self.total_amount = self.get_total_amount()
        super().save(*args, **kwargs)
        
    def get_cancellation_fee(self):
        """
        Calculate cancellation fee based on time before start.
        48+ hours -> 0%
        24-48 hours -> 50%
        <24 hours -> 100%
        """
        if self.status not in ['pending', 'confirmed']:
            return None  # iptal edilemez

        now = timezone.now()
        start_dt = datetime.combine(self.start_date, time.min)

        # timezone aware yap
        if timezone.is_naive(start_dt):
            start_dt = timezone.make_aware(start_dt, timezone.get_current_timezone())

        hours_to_start = (start_dt - now).total_seconds() / 3600

        # toplam tutarı bul
        total = self.total_amount or self.get_total_amount()
        if total is None:
            return None

        if hours_to_start >= 48:
            return Decimal('0.00')
        elif hours_to_start >= 24:
            return total * Decimal('0.50')
        else:
            return total
            