from django.db import models
from authentication.models import User
import uuid

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    message = models.TextField()
    sent = models.BooleanField(default=False)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notification for {self.user.username}: {self.message}"
    
    
class Reminder(models.Model):
    REMINDER_TYPE_CHOICES = (
        ('MEDICINE', 'Medicine'),
        ('APPOINTMENT', 'Appointment'),
        ('TEST', 'Test'),
        ('PAYMENT', 'Payment'),
        ('FOLLOW_UP', 'Follow-up'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reminders')
    reminder_type = models.CharField(max_length=20, choices=REMINDER_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    reminder_time = models.DateTimeField()
    is_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    related_object_id = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['reminder_time']
    
    def __str__(self):
        return f"Reminder for {self.user.username} - {self.title} at {self.reminder_time}"
