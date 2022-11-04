from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('username', 'first_name', 'last_name', 'email', 'receives_alert_emails', 'receives_text_alerts',
                    'is_active', )
    list_per_page = 10
    list_editable = ('receives_alert_emails', 'receives_text_alerts', 'is_active', )
    fieldsets = (
        ('Account and Personal Information',
         {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'text_to_address',
                     'receives_alert_emails', 'receives_text_alerts', )}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions', )}),
        ('Account Login Information', {'fields': ('last_login', 'date_joined', )})
    )


admin.site.register(CustomUser, CustomUserAdmin)
