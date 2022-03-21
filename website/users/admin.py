from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as AuthUserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _

from .forms import UserChangeForm, UserAdminCreationForm

User = get_user_model()


@admin.register(User)
class UserAdmin(AuthUserAdmin):
    form = UserChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
            ('User Profile', {'fields': ('username', 'email', 'password')}),
            (_('Personal info'), {'fields': ('first_name', 'last_name')}),
            (_('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            }),
            (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'full_name', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    ordering = ('username', 'email',)  # Remove username if only email
