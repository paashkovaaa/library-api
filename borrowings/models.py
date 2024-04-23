from datetime import date

from django.core.exceptions import ValidationError
from django.db import models

from books.models import Book
from users.models import User


class Borrowing(models.Model):
    borrow_date = models.DateField(
        default=date.today,
    )
    expected_return_date = models.DateField()
    actual_return_date = models.DateField(
        null=True,
        blank=True,
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="borrowings")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="borrowings")

    @property
    def is_active(self):
        return self.actual_return_date is None

    def clean(self):
        if self.expected_return_date <= self.borrow_date:
            raise ValidationError("Expected return date must be after borrow date.")

        if self.actual_return_date and self.actual_return_date < self.borrow_date:
            raise ValidationError("Actual return date must not be before borrow date.")

    def __str__(self):
        return f"{self.book.title} borrowed by {self.user.email} on {self.borrow_date}"
