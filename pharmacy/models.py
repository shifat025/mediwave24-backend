from django.db import models
from prescriptions.models import Prescription
from authentication.models import User

# Create your models here.
class MedicineOrderStatus(models.TextChoices):
    PENDING = 'pending', 'Pending Confirmation' # User submitted, pharmacy needs to confirm price/availability
    AWAITING_PAYMENT = 'awaiting_payment', 'Awaiting Payment' # Price confirmed, user needs to pay
    CONFIRMED = 'confirmed', 'Confirmed & Processing' # Payment received or COD confirmed
    REJECTED = 'rejected', 'Rejected' # Pharmacy cannot fulfill
    SHIPPED = 'shipped', 'Shipped'
    OUT_FOR_DELIVERY = 'out_for_delivery', 'Out for Delivery'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED_BY_USER = 'cancelled_by_user', 'Cancelled by User'
    CANCELLED_BY_PHARMACY = 'cancelled_by_pharmacy', 'Cancelled by Pharmacy'

class NotificationChannel(models.TextChoices):
    EMAIL = 'email', 'Email'
    SMS = 'sms', 'SMS'
    PUSH = 'push', 'Push Notification'
    IN_APP = 'in_app', 'In-App'


class Pharmacy(models.Model):
    PHARMACY_TYPE_CHOICES = (
        ('RETAIL', 'Retail Pharmacy'),
        ('HOSPITAL', 'Hospital Pharmacy'),
        ('CHAIN', 'Chain Pharmacy'),
        ('ONLINE', 'Online Pharmacy'),
    )
    
    name = models.CharField(max_length=255)
    pharmacy_type = models.CharField(max_length=20, choices=PHARMACY_TYPE_CHOICES)
    license_number = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=17)
    email = models.EmailField()
    is_active = models.BooleanField(default=True)
    operating_hours = models.JSONField()
    delivery_radius_km = models.PositiveIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Pharmacies"
    
    def __str__(self):
        return self.name

class PharmacyStaff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='pharmacy_staff')
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='staff')
    position = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.position} at {self.pharmacy.name}"

class MedicineOrder(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('READY_FOR_PICKUP', 'Ready for Pickup'),
        ('OUT_FOR_DELIVERY', 'Out for Delivery'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('REJECTED', 'Rejected'),
    )
    
    PAYMENT_METHOD_CHOICES = (
        ('CASH', 'Cash on Delivery'),
        ('ONLINE', 'Online Payment'),
        ('INSURANCE', 'Insurance'),
    )
    
    prescription = models.ForeignKey(Prescription, on_delete=models.SET_NULL, null=True, blank=True)
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicine_orders')
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    order_date = models.DateTimeField(auto_now_add=True)
    delivery_address = models.TextField()
    delivery_phone = models.CharField(max_length=17)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    payment_status = models.CharField(max_length=20, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    delivery_charge = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    expected_delivery_date = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    delivery_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    delivery_otp = models.CharField(max_length=6, blank=True)
    notes = models.TextField(blank=True)
    status_hashmap = models.JSONField(default=dict)  # For O(1) status tracking
    
    def __str__(self):
        return f"Order #{self.id} - {self.patient.username} at {self.pharmacy.name}"

class OrderedMedicine(models.Model):
    order = models.ForeignKey(MedicineOrder, on_delete=models.CASCADE, related_name='ordered_items')
    quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    discount_per_unit = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    is_replaced = models.BooleanField(default=False)
    replaced_with = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    replacement_reason = models.TextField(blank=True)
    
    def __str__(self):
        return f"{self.quantity}x {self.inventory.medicine.name} in Order #{self.order.id}"

class PharmacyEarning(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='earnings')
    order = models.ForeignKey(MedicineOrder, on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50)
    status = models.CharField(max_length=20, default='PENDING')  # PENDING, PROCESSED, FAILED
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Earning of {self.amount} for {self.pharmacy.name}"