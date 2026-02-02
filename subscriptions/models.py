from django.db import models
from django.contrib.auth.models import User

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_id = models.CharField(max_length=100, unique=True)  # Moyasar payment ID
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Amount in SAR
    status = models.CharField(max_length=50)  # Payment status (e.g., 'paid', 'failed')
    is_premium = models.BooleanField(default=False)  # Indicates if the user is premium
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp of payment creation

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"