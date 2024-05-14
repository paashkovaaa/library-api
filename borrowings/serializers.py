from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from books.serializers import BookDetailSerializer
from borrowings.models import Borrowing
from borrowings.send_telegram_message import send_telegram_message


class BorrowingDetailSerializer(serializers.ModelSerializer):
    book = BookDetailSerializer()

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
            "user",
        )


class BorrowingListSerializer(BorrowingDetailSerializer):
    @extend_schema_field(serializers.BooleanField)
    def get_is_active(self, obj):
        return obj.is_active

    is_active = serializers.SerializerMethodField("get_is_active")

    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "user",
            "is_active",
        )


class BorrowingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "book",
            "borrow_date",
            "expected_return_date",
        )

    def validate(self, data):
        book = data.get("book")
        if book.inventory == 0:
            raise serializers.ValidationError("This book is out of stock")
        return data

    def create(self, validated_data):
        book = validated_data.get("book")
        book.inventory -= 1
        book.save()

        borrowing = Borrowing.objects.create(
            user=self.context["request"].user,
            **validated_data,
        )

        user = self.context["request"].user
        message = (
            f"New borrowing num.{borrowing.id} created!\n"
            f"Book: {book.title} by {book.author}\n"
            f"User: {user.email}\n"
            f"Borrow Date: {borrowing.borrow_date}\n"
            f"Expected Return Date: {borrowing.expected_return_date}"
        )
        send_telegram_message(message)
        return borrowing
