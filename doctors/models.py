from django.db import models
from authentication.models import User
from autoslug import AutoSlugField
from appointments.models import Appointment

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    national_id_or_passport_number = models.IntegerField()
    registration_number = models.CharField(max_length=40)
    city = models.CharField(max_length=30,blank = True, null = True)
    country = models.CharField(max_length=30,blank = True, null = True)
    doctor_type = models.CharField(max_length=30)
    mobile_number = models.CharField(max_length=11)
    average_rating = models.DecimalField(max_length=30,blank = True, null = True)
    nid_image = models.ImageField(upload_to='doctor/media/uploads', blank = True, null = True)
    created_at= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"
    
class ProfessionalQualification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    degree_name = models.CharField(max_length=30)
    institue_name = models.CharField(max_length=50)
    institue_location = models.CharField(max_length=50)
    passing_year = models.DateField()
    duration = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"

class Department(models.Model):
    doctor = models.ManyToManyField(Doctor)
    name = models.CharField(max_length=30)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)  # AutoSlugField

    def __str__(self):
        return self.name

class Specialization(models.Model):   
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, null=True, blank=True )
    specializanation = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=40)
    certification_type = models.CharField(max_length=30, null = True)   # Traning cirtificat
    document = models.ImageField(upload_to='doctor/media/uploads', blank = True, null = True) #prove to uploading cirtificate

    def __str__(self):
        return self.name
       
    
class Experience(models.Model):
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
    
    doctor = models.ForeignKey(Doctor,  on_delete=models.CASCADE)
    day = models.CharField(max_length=20, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    def __str__(self):
        return f"{self.day}: {self.time_start} - {self.time_end}"


class Fee(models.Model):
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    regular_fee = models.CharField(max_length=30)
    folowup_fee = models.CharField(max_length=30,blank=True,null=True)
    discount_fee = models.CharField(max_length=30,blank=True,null=True)
    free = models.BooleanField(default=False)
    discount = models.BooleanField(default=False)
    followup = models.BooleanField(default=False)
    consultation_duration = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.doctor.user.first_name} {self.doctor.user.last_name}"



    
    


# class WithdrawRequest(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected')
#     ]
#     doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE, related_name='withdraw_requests')
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     requested_at = models.DateTimeField(auto_now_add=True)
#     processed_at = models.DateTimeField(null=True, blank=True)

# class PaymentTransaction(models.Model):
#     transaction_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, default='success')
#     payment_method = models.CharField(max_length=50)  # e.g., Stripe, Card
#     created_at = models.DateTimeField(auto_now_add=True)














