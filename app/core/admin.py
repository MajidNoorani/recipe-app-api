"""
Djanfo admin customization
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from core import models


class UserAdmin(BaseUserAdmin):
    """Define the admin page for users."""
    # list of users page
    ordering = ['id']
    list_display = ['email', 'name',]
    list_filter = ['is_activate', 'is_staff']
    # edit user page
    fieldsets = (
        (
            _('Credentials'),
            {'fields': ('email', 'password',)}
        ),
        (
            _('Permissions'),
            {'fields': ('is_activate',
                        'is_staff',
                        'is_superuser',)}
        ),
        (
            _('Important Dates'),
            {'fields': ('last_login',)}
        ),
    )
    readonly_fields = ['last_login']
    # add user page
    add_fieldsets = (
        (None, {
            'classes': ('wide', ),  # this only changes the page UI
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_activate',
                'is_staff',
                'is_superuser',
            ),
        }),
    )


# we give UserAdmin as one of the arguments of register
# to tell it to apply the changes that we added in the class
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe)
admin.site.register(models.Tag)
