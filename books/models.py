from django.db import models


class Book(models.Model):
    COVER_CHOICES = [("HARD", "Hardcover"), ("SOFT", "Softcover")]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    cover = models.CharField(max_length=4, choices=COVER_CHOICES)
    inventory = models.PositiveIntegerField(default=1)
    daily_fee = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"'{self.title}' by {self.author}"

    class Meta:
        ordering = ("title",)
        unique_together = ("title", "author")
