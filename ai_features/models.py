from django.db import models

# Create your models here.
class Symptom(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    severity = models.PositiveSmallIntegerField(default=1)  # 1-5 scale
    is_common = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class Condition(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)
    is_chronic = models.BooleanField(default=False)
    severity = models.PositiveSmallIntegerField(default=1)  # 1-5 scale
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class SymptomConditionMapping(models.Model):
    symptom = models.ForeignKey(Symptom, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    probability_score = models.DecimalField(max_digits=5, decimal_places=2)  # 0-1 scale
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('symptom', 'condition')
    
    def __str__(self):
        return f"{self.symptom.name} ➝ {self.condition.name} ({self.probability_score})"

class ChatSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_sessions')
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    metadata = models.JSONField(blank=True, null=True)
    
    def __str__(self):
        return f"Chat Session #{self.session_id} - {self.user.username}"

class ChatMessage(models.Model):
    SENDER_CHOICES = (
        ('USER', 'User'),
        ('BOT', 'Bot'),
        ('DOCTOR', 'Doctor'),
        ('SUPPORT', 'Support'),
    )
    
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender_type = models.CharField(max_length=10, choices=SENDER_CHOICES)
    sender_id = models.CharField(max_length=50)  # Could be user ID or bot ID
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(blank=True, null=True)
    
    class Meta:
        ordering = ['timestamp']
    
    def __str__(self):
        return f"Message in Session #{self.session.session_id} from {self.sender_type}"

class SupportTicket(models.Model):
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    )
    
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
        ('URGENT', 'Urgent'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='support_tickets')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    subject = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    related_object_id = models.CharField(max_length=50, blank=True)
    related_object_type = models.CharField(max_length=50, blank=True)
    
    def __str__(self):
        return f"Ticket #{self.id} - {self.subject} ({self.status})"

class TicketResponse(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    is_internal_note = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    attachments = models.JSONField(blank=True, null=True)  # List of file URLs
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Response to Ticket #{self.ticket.id} by {self.responder.username if self.responder else 'System'}"