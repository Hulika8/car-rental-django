from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from django.contrib import messages
from datetime import date
from .models import Reservation


class ReservationAdminForm(forms.ModelForm):
    """
    Custom form for Reservation Admin
    Adds automatic calculation for daily_rate and total_amount
    """
    
    class Meta:
        model = Reservation
        fields = '__all__'
        widgets = {
            'daily_rate': forms.NumberInput(attrs={'style': 'background-color: #fff3cd; color: #000; font-weight: bold; font-size: 14px;'}),
            'total_amount': forms.NumberInput(attrs={'style': 'background-color: #d4edda; color: #000; font-weight: bold; font-size: 14px;'}),
        }
        
    class Media:
        js = ('admin/js/reservation_auto_calculate.js',)


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    form = ReservationAdminForm
    
    list_display = ('user', 'car', 'start_date', 'end_date', 'get_duration_days', 'daily_rate', 'total_amount', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'car__brand', 'car__model')
    search_help_text = 'Search by username, car brand, or model'
    date_hierarchy = 'created_at'
    ordering = ('-created_at',)
    list_per_page = 10
    list_max_show_all = 100
    list_editable = ('status',)
    list_display_links = ('user', 'car')
    list_select_related = ('user', 'car')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'car', 'start_date', 'end_date', 'daily_rate', 'total_amount', 'status')
        }),
        ('Advanced', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_duration_days(self, obj):
        return obj.get_duration_days()
    get_duration_days.short_description = "Duration (Days)"
    
    def get_total_amount(self, obj):
        return f"${obj.get_total_amount():.2f}"
    get_total_amount.short_description = "Total Amount (USD)"
    
    def save_model(self, request, obj, form, change):
        """
        Override save_model to automatically fill daily_rate and total_amount
        Also set status to 'confirmed' if admin is creating the reservation
        Validates status transitions
        """
        # Auto-fill daily_rate from selected car
        if obj.car:
            obj.daily_rate = obj.car.daily_price
        
        # Auto-calculate total_amount
        if obj.start_date and obj.end_date and obj.daily_rate:
            duration = (obj.end_date - obj.start_date).days
            obj.total_amount = obj.daily_rate * duration
        
        # STATUS MANAGEMENT
        if change:  # Updating existing reservation
            old_obj = Reservation.objects.get(pk=obj.pk)
            
            # Check if changing to 'active' from any other status
            if old_obj.status != 'active' and obj.status == 'active':
                # Validate: Can only activate if start date has arrived
                if obj.start_date > date.today():
                    messages.error(
                        request,
                        f"Cannot activate reservation! Start date is {obj.start_date}, today is {date.today()}"
                    )
                    obj.status = old_obj.status  # Revert to old status
                    
                # Validate: End date must not be in the past
                elif obj.end_date < date.today():
                    messages.warning(
                        request,
                        f"⚠️ End date is {obj.end_date} (past). Auto-setting status to 'completed'."
                    )
                    obj.status = 'completed'
                    
                # Validate: No other active reservation for same car
                elif Reservation.objects.filter(
                    car=obj.car,
                    status='active',
                ).exclude(pk=obj.pk).exists():
                    messages.error(
                        request,
                        f"❌ Car {obj.car} already has an active reservation!"
                    )
                    obj.status = old_obj.status
            # Check if changing to 'cancelled'
            if obj.status == 'cancelled':
                if old_obj.status not in ['pending', 'confirmed']:
                    messages.error(
                        request,
                        f"❌ Cannot cancel! Only pending/confirmed reservations can be cancelled. Current: {old_obj.status}"
                    )
                    obj.status = old_obj.status
                        
                    
        else:  # Creating new reservation
            # If admin is creating reservation, set status to 'confirmed'
            obj.status = 'confirmed'
        
        super().save_model(request, obj, form, change)