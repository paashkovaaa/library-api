from django.test import TestCase
from rest_framework import status
from django.urls import reverse
from datetime import date
from django.contrib.auth import get_user_model
from books.models import Book
from rest_framework.test import APIClient
from borrowings.models import Borrowing


class BorrowingViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="testpass123"
        )

        self.admin = get_user_model().objects.create_superuser(
            email="admin@example.com", password="adminpass123"
        )

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            cover="HARD",
            inventory=5,
            daily_fee=2.00,
        )

        self.borrowing = Borrowing.objects.create(
            book=self.book,
            user=self.user,
            expected_return_date=date(2024, 12, 31),
        )

    def test_list_borrowings(self):
        self.client.force_authenticate(self.user)

        url = reverse("borrowings:borrowings-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_borrowings_admin(self):
        self.client.force_authenticate(self.admin)

        url = reverse("borrowings:borrowings-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_borrowing(self):
        self.client.force_authenticate(self.user)

        payload = {
            "book": self.book.id,
            "borrow_date": date(2024, 1, 1),
            "expected_return_date": date(2024, 12, 31),
        }

        url = reverse("borrowings:borrowings-list")
        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["book"], self.book.id)

    def test_return_borrowing(self):
        self.client.force_authenticate(self.user)

        url = reverse(
            "borrowings:borrowings-return-borrowing", args=[self.borrowing.id]
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["detail"], "Borrowing returned successfully.")

        self.book.refresh_from_db()
        self.assertEqual(self.book.inventory, 6)

    def test_return_borrowing_already_returned(self):
        self.borrowing.actual_return_date = date.today()
        self.borrowing.save()

        self.client.force_authenticate(self.user)

        url = reverse(
            "borrowings:borrowings-return-borrowing", args=[self.borrowing.id]
        )
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "This borrowing has already been returned."
        )

    def test_user_filter_access_restriction(self):
        self.client.force_authenticate(self.user)

        url = reverse("borrowings:borrowings-list") + "?user=1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
