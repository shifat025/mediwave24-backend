from django.db import models
from django.contrib.auth.models import User
from doctors.models import Doctor
from django.contrib.postgres.fields import JSONField 
# Create your models here.

class Patient(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='patient/media/uploads', blank = True, null = True)
    name = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    relation = models.CharField(max_length=10)
    hight = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    bloodgroup = models.CharField(max_length=10)
    contact_phone = models.CharField(max_length=17, blank=True)

class HealthReport(models.Model):
    REPORT_TYPE_CHOICES = (
    ('daily', 'Daily'),
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
)


    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='health_reports')  # Reference to the patient this report belongs to
    report_type = models.CharField( max_length=10,choices=REPORT_TYPE_CHOICES )  # Type of the report (daily, weekly, monthly)
    start_date = models.DateField()  # Start of reporting period
    end_date = models.DateField()    # End of reporting period
    summary_data = JSONField(default=dict)  # Aggregated health data in JSON format
    generated_at = models.DateTimeField(auto_now_add=True)  # When the report was generated
    created_at = models.DateTimeField(auto_now_add=True)    # When the record was created
    updated_at = models.DateTimeField(auto_now=True)   

star_choice = [
    ('⭐','1'),
    ('⭐⭐','2'),
    ('⭐⭐⭐','3'),
    ('⭐⭐⭐⭐','4'),
    ('⭐⭐⭐⭐⭐','5'),
]

class Review(models.Model):
    reviewer = models.ForeignKey(Patient, on_delete=models.CASCADE)
    docter = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    review = models.TextField()
    ratting = models.CharField(choices=star_choice,max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Patient: {self.reviewer.user.first_name}; Doctor: {self.docter.user.first_name}"