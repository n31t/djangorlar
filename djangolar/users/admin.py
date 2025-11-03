from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUserAbstractUser


@admin.register(CustomUserAbstractUser)
class CustomUserAbstractUserAdmin(BaseUserAdmin):
    list_display = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'is_staff', 'is_active']
    list_filter = ['is_staff', 'is_superuser', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'phone_number']
    ordering = ['username']
    
    fieldsets = BaseUserAdmin.fieldsets + (
        (_('Additional Information'), {
            'fields': ('phone_number', 'date_of_birth', 'bio')
        }),
    )
    
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (_('Additional Information'), {
            'fields': ('phone_number', 'date_of_birth')
        }),
    )
