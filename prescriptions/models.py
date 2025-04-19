from django.db import models
from authentication.models import User
from doctors.models import Doctor
from appointments.models import Appointment
from patients.models import Patient

class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, related_name='prescriptions', null=True, blank=True)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='prescriptions')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='prescriptions')
    diagnosis = models.TextField()
    notes = models.TextField(blank=True)
    date_issued = models.DateTimeField(auto_now_add=True)
    follow_up_date = models.DateField(null=True, blank=True)
    follow_up_notes = models.TextField(blank=True)
    file = models.FileField(upload_to='prescriptions/', null=True, blank=True)
    test_suggestions = models.TextField(blank=True, null=True, help_text="Suggested lab tests (link to labs if integrated)")
    graph_representation = models.JSONField(null=True, blank=True)  # For symptom->diagnosis->prescription graph

    def __str__(self):
        return f"Prescription #{self.id} for {self.patient.user.get_full_name()} by Dr. {self.doctor.user.get_full_name()}"

class Medicine(models.Model):
    name = models.CharField(max_length=255)
    generic_name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    dosage_forms = models.CharField(max_length=50, choices=[
        ('TABLET', 'Tablet'),
        ('CAPSULE', 'Capsule'),
        ('SYRUP', 'Syrup'),
        ('INJECTION', 'Injection'),
        ('OINTMENT', 'Ointment'),
        ('DROPS', 'Drops'),
        ('INHALER', 'Inhaler'),
        ('OTHER', 'Other')
    ])
DURATION_UNIT_CHOICES = [
        ('DAYS', 'Days'),
        ('WEEKS', 'Weeks'),
        ('MONTHS', 'Months'),
        ('UNTIL_FINISHED', 'Until Finished'),
    ]

FREQUENCY_CHOICES = [
        ('OD', 'Once Daily'),
        ('BD', 'Twice Daily'),
        ('TDS', 'Three Times Daily'),
        ('QDS', 'Four Times Daily'),
        ('Q4H', 'Every 4 Hours'),
        ('Q6H', 'Every 6 Hours'),
        ('Q8H', 'Every 8 Hours'),
        ('Q12H', 'Every 12 Hours'),
        ('PRN', 'As Required'),
    ]
    
class PrescribedMedicine(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='medicines')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    dosage = models.CharField(max_length=100)  # e.g., "1 tablet twice daily"
    duration = models.CharField(max_length=100)  # e.g., "7 days"
    duration_unit = models.CharField(max_length=10, choices=DURATION_UNIT_CHOICES)
    instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.medicine.name} for {self.prescription.patient.user.get_full_name()}"
 

class MedicalTest(models.Model):
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='tests')
    test_name = models.CharField(max_length=255)
    notes = models.TextField(blank=True)

    def __str__(self):
        return self.test_name


    
class TestResult(models.Model):
    prescribed_test = models.OneToOneField(MedicalTest, on_delete=models.CASCADE, related_name='result')
    result_file = models.FileField(upload_to='test_results/')
    notes = models.TextField(blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Result for {self.prescribed_test.test.name}"


class PharmacyOrder(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PRICE_CONFIRMED', 'Price Confirmed'),
        ('PAID', 'Paid'),
        ('PROCESSING', 'Processing'),
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
    )
    
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE, related_name='pharmacy_orders')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='medicine_orders')
    pharmacy = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    payment_method = models.CharField(max_length=50, blank=True)
    delivery_address = models.TextField()
    expected_delivery_date = models.DateField(null=True, blank=True)
    delivery_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    delivery_otp = models.CharField(max_length=6, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status_hashmap = models.JSONField(default=dict)  # For O(1) status tracking

