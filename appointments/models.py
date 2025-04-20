from django.db import models
from authentication.models import User
from doctors.models import Doctor,AvailableTime
from patients.models import Patient
import uuid

# Create your models here.
Appointment_Status = [
    ('Completed','Completed'),
    ('Pending','Pending'),
    ('Running','Running'),
    ('cancelled', 'Cancelled'),
    ("rescheduled", "Rescheduled"),
    ('MISSED', 'Missed')
]


class Appointment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient,on_delete=models.CASCADE)
    docter = models.ForeignKey(Doctor,on_delete=models.CASCADE)
    appointment_status = models.CharField(choices=Appointment_Status,max_length=15,default='Pending')
    symptoms = models.TextField()
    appointment_time = models.ForeignKey(AvailableTime,on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)
    meeting_link = models.URLField(blank=True, null=True)
    is_followup = models.BooleanField(default=False)
    cancel = models.BooleanField(default=False)
    cancellation_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Doctor : {self.docter.user.first_name}, Patient : {self.patient.user.first_name}"
    
class AppointmentReschedule(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='reschedules')
    original_time = models.ForeignKey(AvailableTime, on_delete=models.SET_NULL, null=True, related_name='original_reschedules')
    new_time = models.ForeignKey(AvailableTime, on_delete=models.SET_NULL, null=True, related_name='new_reschedules')
    reason = models.TextField(blank=True)
    requested_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, choices=[('PENDING', 'Pending'), ('APPROVED', 'Approved'), ('REJECTED', 'Rejected')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reschedule request for {self.appointment}"






