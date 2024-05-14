from rest_framework import serializers

from books.models import Book


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author", "cover", "inventory", "daily_fee")


class BookListSerializer(BookDetailSerializer):
    class Meta:
        model = Book
        fields = ("id", "title", "author")
