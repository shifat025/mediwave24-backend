
import pyotp
from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.validators import  EmailValidator


GENDER_CHOICES = [
    ('male', 'Male'),
    ('female', 'Female'),
]

ROLE_CHOICES = [
    ("admin", "Admin"),
    ("doctor", "Doctor"),
    ("pharmacy", "Pharmacy"),
    ("support", "Support"),
    ("user", "User"),
    ("delivery", "Delivery"),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email= email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True,validators=[EmailValidator()],error_messages={ 'unique': "A user with that email already exists.", })
    first_name= models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20, blank=True)
    gender = models.CharField(max_length=10,  choices= GENDER_CHOICES,null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user")
    address = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    
    # Permissions
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_password_change = models.DateTimeField(blank=True, null=True)
    
    # 2FA
    otp_enabled = models.BooleanField(default=False)
    otp_base32 = models.CharField(max_length=64,  default=lambda: pyotp.random_base32(), blank=True)
    
    # Login Security
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    last_login_device = models.TextField(null=True, blank=True)
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    @property
    def is_verified(self):
        # Check if OTP is enabled and if user has any active trusted devices
        return self.otp_enabled and self.device_activities.filter(is_active=True).exists()

    def verify_otp(self, otp):
        totp = pyotp.TOTP(self.otp_base32)
        return totp.verify(otp)
    

#  Device model to store information about devices used by the user for security and login tracking.
class UserDeviceActivity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='device_activities')
    device_name = models.CharField(max_length=100)  # Device name (e.g., Chrome on Windows)
    device_type = models.CharField(max_length=50, blank=True)   # Type of device (e.g., mobile, desktop)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # IP address used for login
    last_used_at = models.DateTimeField(null=True, blank=True)  # Last time the device was used
    created_at = models.DateTimeField(auto_now_add=True) # Device creation time
    is_active = models.BooleanField(default=True)   # Whether the device is active or not (for logout functionality)
    user_agent = models.TextField(blank=True, null=True)  # User agent string (browser and OS info)
    location = models.CharField(max_length=200, blank=True, null=True)  # User agent string (browser and OS info)
    login_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Device Activity"
        verbose_name_plural = "Device Activities"
        ordering = ['-last_used_at']

    def __str__(self):
        return f"{self.user.email} - {self.device_name}"



class SecurityAlert(models.Model):
    ALERT_TYPE_CHOICES = [
    ('SUSPICIOUS_LOGIN', 'Suspicious Login Attempt'),
    ('MULTIPLE_FAILED_LOGINS', 'Multiple Failed Logins'),
    ('DEVICE_CHANGE', 'Login from New Device'),
    ('GEO_CHANGE', 'Login from New Location'),
    ('PASSWORD_CHANGE', 'Password Changed'),
    ('TWO_FACTOR_DISABLED', 'Two Factor Disabled'),
]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="security_alerts")
    alert_type = models.CharField(max_length=50, choices=ALERT_TYPE_CHOICES)
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    device_info = models.JSONField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    resolved = models.BooleanField(default=False)
    resolved_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Security Alert"
        verbose_name_plural = "Security Alerts"

    def __str__(self):
        return f"{self.user} - {self.alert_type}"
