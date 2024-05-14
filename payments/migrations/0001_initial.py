# Generated by Django 4.2 on 2024-05-14 12:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("borrowings", "0002_rename_book_id_borrowing_book_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[("Pending", "Pending"), ("Paid", "Paid")],
                        default="Pending",
                        max_length=10,
                    ),
                ),
                (
                    "type",
                    models.CharField(
                        choices=[("Payment", "Payment"), ("Fine", "Fine")],
                        max_length=10,
                    ),
                ),
                ("session_url", models.URLField(blank=True, null=True)),
                ("session_id", models.CharField(blank=True, max_length=100, null=True)),
                (
                    "money_to_pay",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
                (
                    "borrowing",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="payments",
                        to="borrowings.borrowing",
                    ),
                ),
            ],
        ),
    ]
