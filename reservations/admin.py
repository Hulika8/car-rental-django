from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
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
    raw_id_fields = ('user', 'car')
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