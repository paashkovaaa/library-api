from django.test import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookListSerializer, BookDetailSerializer

BOOK_URL = reverse("books:books-list")


def detail_url(book_id):
    return reverse("books:books-detail", args=[book_id])


class UnauthenticatedOrNotAdminBooksTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "user1@test.com",
            "testpassword",
        )
        self.client.force_authenticate(self.user)
        self.book1 = Book.objects.create(
            title="Test",
            author="Author1",
            cover="HARD",
            inventory=1,
            daily_fee=2.00,
        )
        self.book2 = Book.objects.create(
            title="Book",
            author="Author2",
            cover="SOFT",
            inventory=3,
            daily_fee=4.00,
        )

    def test_list_books(self):
        res = self.client.get(BOOK_URL)

        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_by_title(self):
        res = self.client.get(BOOK_URL, {"title": "Test"})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]["title"], "Test")

    def test_retrieve_book_detail(self):
        book = self.book1
        url = detail_url(book.id)
        res = self.client.get(url)

        serializer = BookDetailSerializer(book)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_forbidden(self):
        payload = {
            "title": "Test Book",
            "author": "Author",
            "cover": "SOFT",
            "inventory": 4,
            "daily_fee": 5.00,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_forbidden(self):
        payload = {
            "title": "Updated Book",
            "author": "New Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 8.00,
        }
        book = self.book1
        url = detail_url(book.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_book_forbidden(self):
        book = self.book1
        url = detail_url(book.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminBooksTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)
        self.book1 = Book.objects.create(
            title="Test",
            author="Author1",
            cover="HARD",
            inventory=1,
            daily_fee=2.00,
        )

    def test_create_book(self):
        payload = {
            "title": "Test Book",
            "author": "Author",
            "cover": "SOFT",
            "inventory": 4,
            "daily_fee": 5.00,
        }
        res = self.client.post(BOOK_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_update_book(self):
        payload = {
            "title": "Updated Book",
            "author": "New Author",
            "cover": "HARD",
            "inventory": 10,
            "daily_fee": 8.00,
        }

        book = self.book1
        url = detail_url(book.id)
        res = self.client.put(url, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_book(self):
        book = self.book1
        url = detail_url(book.id)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
