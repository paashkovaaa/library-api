# Generated by Django 5.0.4 on 2024-04-22 12:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("borrowings", "0001_initial"),
    ]

    operations = [
        migrations.RenameField(
            model_name="borrowing",
            old_name="book_id",
            new_name="book",
        ),
        migrations.RenameField(
            model_name="borrowing",
            old_name="user_id",
            new_name="user",
        ),
    ]