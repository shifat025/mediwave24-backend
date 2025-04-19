from django.db import models

# Create your models here.
class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="admin_profile")
    roles = models.JSONField()  # e.g., ["customer care", "salesman"]

    def __str__(self):
        return f"Admin: {self.user.username}"


class SystemAnalytics(models.Model):
    total_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    daily_earnings = models.DecimalField(max_digits=10, decimal_places=2)
    most_common_diseases = models.TextField()  # e.g., ["flu", "covid"]
    date = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Analytics for {self.date}"
