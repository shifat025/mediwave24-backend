import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone
from authentication.models import User
from doctors.models import Doctor

# ========== ENUMS ==========
REFUND_STATUS = [
        ('REQUESTED', 'Requested'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]
PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED', 'Failed'),
        ('REFUNDED', 'Refunded'),
        ('PARTIALLY_REFUNDED', 'Partially Refunded'),
    ]
    
WITHDRAWAL_STATUS = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('REJECTED', 'Rejected'),
    ]

# ========== PAYMENT ==========
class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.SET_NULL, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='PENDING')
    gateway_transaction_id = models.CharField(max_length=255, blank=True, null=True)
    gateway_response = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Payment {self.id} - {self.status}"

# ========== REFUND ==========
class Refund(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    payment = models.OneToOneField(Payment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reason = models.TextField()
    initiated_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=REFUND_STATUS, default='REQUESTED')

    def __str__(self):
        return f"Refund for {self.payment.id}"

# ========== DOCTOR EARNINGS ==========
class DoctorEarnings(models.Model):
    doctor = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'DOCTOR'}, on_delete=models.CASCADE)
    appointment = models.ForeignKey('appointments.Appointment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    platform_fee = models.DecimalField(max_digits=10, decimal_places=2)
    net_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Earnings for Dr. {self.doctor.get_full_name()}"

# ========== WITHDRAWAL REQUEST ==========
class WithdrawalRequest(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, limit_choices_to={'role': 'DOCTOR'}, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=WITHDRAWAL_STATUS, default='PENDING')
    processed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='processed_withdrawals', on_delete=models.SET_NULL)
    transaction_details = models.JSONField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Withdrawal by Dr. {self.doctor.get_full_name()} - {self.status}"

# ========== FINANCIAL REPORT (Optional) ==========
# class FinancialReport(models.Model):
#     report_date = models.DateField(default=timezone.now)
#     total_revenue = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
#     total_expenses = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
#     doctor_payouts = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
#     generated_by = models.ForeignKey(Doctor, on_delete=models.SET_NULL, null=True)
#     notes = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Financial Report - {self.report_date}"
    
# class FinancialReport(models.Model):
#     REPORT_TYPES = [
#         ('DAILY', 'Daily'),
#         ('WEEKLY', 'Weekly'),
#         ('MONTHLY', 'Monthly'),
#         ('YEARLY', 'Yearly'),
#         ('CUSTOM', 'Custom'),
#     ]
    
#     report_type = models.CharField(max_length=10, choices=REPORT_TYPES)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     total_revenue = models.DecimalField(max_digits=15, decimal_places=2)
#     total_expenses = models.DecimalField(max_digits=15, decimal_places=2, default=0)
#     net_profit = models.DecimalField(max_digits=15, decimal_places=2)
#     appointment_earnings = models.DecimalField(max_digits=15, decimal_places=2)
#     pharmacy_earnings = models.DecimalField(max_digits=15, decimal_places=2)
#     doctor_payouts = models.DecimalField(max_digits=15, decimal_places=2)
#     refunds = models.DecimalField(max_digits=15, decimal_places=2)
#     generated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
#     generated_at = models.DateTimeField(auto_now_add=True)
#     notes = models.TextField(blank=True)
#     pdf_file = models.FileField(upload_to='financial_reports/', null=True, blank=True)
    
#     class Meta:
#         ordering = ['-end_date']
    
#     def __str__(self):
#         return f"{self.get_report_type_display()} Report ({self.start_date} to {self.end_date})"
        




