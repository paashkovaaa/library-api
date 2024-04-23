from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from books.seralizers import BookDetailSerializer
from borrowings.models import Borrowing


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
