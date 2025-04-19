# from django.db import models

# # Create your models here.
# class SystemAnalytic(models.Model):
#     METRIC_CHOICES = (
#         ('TOTAL_USERS', 'Total Users'),
#         ('ACTIVE_USERS', 'Active Users'),
#         ('NEW_USERS', 'New Users'),
#         ('TOTAL_DOCTORS', 'Total Doctors'),
#         ('ACTIVE_DOCTORS', 'Active Doctors'),
#         ('TOTAL_APPOINTMENTS', 'Total Appointments'),
#         ('COMPLETED_APPOINTMENTS', 'Completed Appointments'),
#         ('TOTAL_ORDERS', 'Total Orders'),
#         ('COMPLETED_ORDERS', 'Completed Orders'),
#         ('REVENUE', 'Revenue'),
#         ('DOCTOR_EARNINGS', 'Doctor Earnings'),
#         ('PHARMACY_EARNINGS', 'Pharmacy Earnings'),
#         ('PLATFORM_EARNINGS', 'Platform Earnings'),
#         ('REFUNDS', 'Refunds'),
#         ('AVG_RATING', 'Average Rating'),
#     )
    
#     metric = models.CharField(max_length=50, choices=METRIC_CHOICES)
#     value = models.DecimalField(max_digits=20, decimal_places=2)
#     date_recorded = models.DateField()
#     time_period = models.CharField(max_length=20)  # daily, weekly, monthly
#     metadata = models.JSONField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('metric', 'date_recorded', 'time_period')
    
#     def __str__(self):
#         return f"{self.get_metric_display()} on {self.date_recorded} ({self.time_period})"

# class DiseaseAnalytic(models.Model):
#     condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
#     occurrence_count = models.PositiveIntegerField()
#     date_recorded = models.DateField()
#     time_period = models.CharField(max_length=20)  # daily, weekly, monthly
#     age_group_distribution = models.JSONField(blank=True, null=True)
#     gender_distribution = models.JSONField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     class Meta:
#         unique_together = ('condition', 'date_recorded', 'time_period')
    
#     def __str__(self):
#         return f"{self.condition.name} - {self.occurrence_count} cases on {self.date_recorded}"

# class SystemSetting(models.Model):
#     SETTING_CHOICES = (
#         ('APPOINTMENT_MIN_DURATION', 'Minimum Appointment Duration (minutes)'),
#         ('APPOINTMENT_MAX_ADVANCE_DAYS', 'Maximum Days to Book in Advance'),
#         ('MIN_WITHDRAWAL_AMOUNT', 'Minimum Withdrawal Amount'),
#         ('MAX_WITHDRAWAL_AMOUNT', 'Maximum Withdrawal Amount'),
#         ('PLATFORM_FEE_PERCENTAGE', 'Platform Fee Percentage'),
#         ('CANCELLATION_WINDOW_HOURS', 'Cancellation Window (hours)'),
#         ('RESCHEDULE_LIMIT', 'Maximum Reschedule Attempts'),
#         ('OTP_EXPIRY_MINUTES', 'OTP Expiry Time (minutes)'),
#         ('SESSION_TIMEOUT_MINUTES', 'Session Timeout (minutes)'),
#     )
    
#     setting_key = models.CharField(max_length=50, choices=SETTING_CHOICES, unique=True)
#     setting_value = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return f"{self.get_setting_key_display()}: {self.setting_value}"

# class SystemLog(models.Model):
#     LOG_LEVEL_CHOICES = (
#         ('DEBUG', 'Debug'),
#         ('INFO', 'Info'),
#         ('WARNING', 'Warning'),
#         ('ERROR', 'Error'),
#         ('CRITICAL', 'Critical'),
#     )
    
#     COMPONENT_CHOICES = (
#         ('AUTH', 'Authentication'),
#         ('APPOINTMENT', 'Appointment'),
#         ('PAYMENT', 'Payment'),
#         ('PHARMACY', 'Pharmacy'),
#         ('NOTIFICATION', 'Notification'),
#         ('AI', 'AI Service'),
#         ('API', 'API'),
#         ('BACKGROUND', 'Background Task'),
#         ('SYSTEM', 'System'),
#     )
    
#     timestamp = models.DateTimeField(auto_now_add=True)
#     level = models.CharField(max_length=10, choices=LOG_LEVEL_CHOICES)
#     component = models.CharField(max_length=20, choices=COMPONENT_CHOICES)
#     message = models.TextField()
#     details = models.JSONField(blank=True, null=True)
#     trace = models.TextField(blank=True)
    
#     class Meta:
#         ordering = ['-timestamp']
    
#     def __str__(self):
#         return f"[{self.level}] {self.component} - {self.message[:100]}"