from django.db import models
from authentication.models import User
from autoslug import AutoSlugField
import uuid

# Create your models here.
class Doctor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    national_id_or_passport_number = models.IntegerField()
    registration_number = models.CharField(max_length=40)
    city = models.CharField(max_length=30,blank = True, null = True)
    country = models.CharField(max_length=30,blank = True, null = True)
    doctor_type = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=11)
    nid_image = models.ImageField(upload_to='doctor/media/uploads', blank = True, null = True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    
class ProfessionalQualification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=30)
    institue_name = models.CharField(max_length=50)
    institue_location = models.CharField(max_length=50)
    passing_year = models.DateField()
    duration = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ManyToManyField(Doctor)
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)  # AutoSlugField

    def __str__(self):
        return self.name

class Specialization(models.Model):  
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) 
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True )
    specializanation = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=40)
    certification_type = models.CharField(max_length=30, null = True)   # Traning cirtificat
    document = models.ImageField(upload_to='doctor/media/uploads', blank = True, null = True) #prove to uploading cirtificate

    def __str__(self):
        return self.name
       
    
class Experience(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    hosspital_name = models.CharField(max_length=50)
    designation = models.CharField(max_length=30)
    department = models.CharField(max_length=30)
    employee_period_start = models.DateField()
    employee_period_end = models.DateField()
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"
    
class AvailableTime(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.ForeignKey(Doctor,  on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.day}: {self.time_start} - {self.time_end}"


class Fee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    regular_fee = models.CharField(max_length=30)
    followup_fee = models.CharField(max_length=30,blank=True,null=True)
    discount_fee = models.CharField(max_length=30,blank=True,null=True)
    free = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"
















