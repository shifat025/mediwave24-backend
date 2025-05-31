from django.contrib import admin
from django.contrib.auth.forms import  AdminPasswordChangeForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User, SecurityAlert, UserDeviceActivity
# Register your models here.
class CustomUserAdmin(BaseUserAdmin):
    model = User
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_active', 'date_joined')
    list_filter = ('is_active', 'is_staff', 'role')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)

    # Use default password change form
    change_password_form = AdminPasswordChangeForm
    # Exclude the date_joined field from being editable in the form
    fieldsets = (
        ('Personal info', {'fields': ('email', 'first_name', 'last_name','phone', 'gender', 'date_of_birth', 'address', 'profile_image')}),
        ('Password', {'fields': ('password','last_password_change',)}),
        ('2FA', {'fields': ('otp_enabled', 'otp_base32')}),
        ('Security', {'fields': ('last_login_ip', 'last_login_device')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'role', 'groups', 'user_permissions')}),
    )

    # Customize add fieldsets
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, CustomUserAdmin)
admin.site.register(SecurityAlert)   
admin.site.register(UserDeviceActivity)   
