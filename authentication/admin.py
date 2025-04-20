from django.contrib import admin
from .models import User, SecurityAlert, UserDeviceActivity
# Register your models here.
admin.site.register(User)   
admin.site.register(SecurityAlert)   
admin.site.register(UserDeviceActivity)   
