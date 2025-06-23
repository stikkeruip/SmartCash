from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined', 'two_factor_enabled')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'is_email_verified', 'phone_number', 'date_of_birth')}),
        ('Address', {'fields': ('address_line1', 'address_line2', 'city', 'postal_code', 'country')}),
        ('Bank Integration', {'fields': ('piraeus_customer_id', 'bank_consent_ids', 'preferred_sca_method')}),
        ('Security', {'fields': ('failed_login_attempts', 'account_locked_until', 'two_factor_enabled')}),
        ('Preferences', {'fields': ('language', 'currency', 'timezone_field')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'first_name', 'last_name', 'password1', 'password2'),
        }),
    )


admin.site.register(User, UserAdmin)
