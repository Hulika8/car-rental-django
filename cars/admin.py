from django.contrib import admin

from .models import Car

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ('brand', 'model', 'year', 'color', 'get_daily_price_display', 'in_fleet', 'is_rented', 'is_damaged', 'is_maintenance', 'image', 'created_at', 'updated_at')
    list_filter = ('brand', 'model', 'year', 'color', 'daily_price', 'in_fleet', 'is_rented', 'is_damaged', 'is_maintenance')
    search_fields = ('brand', 'model', 'year', 'color')
    list_editable = ('in_fleet', 'is_rented', 'is_damaged', 'is_maintenance')
    list_per_page = 10
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('brand', 'model', 'year', 'color', 'daily_price', 'in_fleet', 'is_rented', 'is_damaged', 'is_maintenance', 'image')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    search_help_text = "Search by brand, model, year, or color"
    empty_value_display = "N/A"