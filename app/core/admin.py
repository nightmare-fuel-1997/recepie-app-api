"""
Django admin customization for the core app.
"""
# Django's admin site registration module
from django.contrib import admin
# Import Django's default UserAdmin class and rename it to BaseUserAdmin
# so we can extend it with custom functionality for our user model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# Import the custom User model from the core app
from core import models
# Register the custom User model with the admin site
from django.utils.translation import gettext_lazy as _
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        # (
        #     _('Personal Info'),
        #     {
        #         'fields': (
        #             'is_active',
        #             'is_staff',
        #             'is_superuser',
        #         )
        #     }
        # ),
        (_('Important Dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ['last_login']

admin.site.register(models.User, UserAdmin)
