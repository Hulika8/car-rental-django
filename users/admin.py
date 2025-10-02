from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'phone', 'city', 'state', 'is_verified', 'is_active', 'created_at')
    list_filter = ('is_verified', 'is_active', 'city', 'state', 'created_at')
    search_fields = ('user__username', 'user__email', 'user__first_name', 'user__last_name', 'phone', 'license_number')
    list_editable = ('is_verified', 'is_active')
    list_per_page = 10
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('user', 'phone', 'address', 'city', 'state', 'zip_code', 'license_number', 'date_of_birth', 'is_verified', 'is_active')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    search_help_text = "Search by username, email, name, phone, or license number"
    empty_value_display = "N/A"

