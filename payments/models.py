from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

from borrowings.models import Borrowing


class Payment(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Paid", "Paid"),
    ]
    TYPE_CHOICES = [("Payment", "Payment"), ("Fine", "Fine")]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="Pending")
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    borrowing = models.OneToOneField(
        Borrowing, on_delete=models.CASCADE, related_name="payments"
    )
    session_url = models.URLField(blank=True, null=True)
    session_id = models.CharField(max_length=100, blank=True, null=True)
    money_to_pay = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Payment {self.id}: {self.status} for borrowing {self.borrowing.id}"


@receiver(pre_save, sender=Payment)
def update_payment(sender, instance, **kwargs):
    if instance.borrowing.actual_return_date:
        borrowing_duration = (instance.borrowing.actual_return_date - instance.borrowing.borrow_date).days
        instance.money_to_pay = borrowing_duration * instance.borrowing.book.daily_fee
