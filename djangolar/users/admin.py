from django.contrib import admin
from django.contrib.admin import register, ModelAdmin
from django.utils.translation import gettext_lazy as _

from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAbstractUserAdmin(ModelAdmin):
    list_display = (
        "email",
        "full_name",
        "is_active",
        "is_staff",
        "is_superuser",
    )
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('email', 'full_name')
    ordering = ('-date_joined',)
