import uuid
from unittest import TestCase

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from users.serializers import UserSerializer

USER_URL = reverse("users:create")
ME_URL = reverse("users:manage")


class UserTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        unique_email = f"user_{uuid.uuid4()}@test.com"

        self.user = get_user_model().objects.create_user(
            unique_email,
            "testpassword",
        )
        self.client.force_authenticate(self.user)

    def test_create_user(self):
        payload = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "strongpassword123",
        }
        res = self.client.post(USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_retrieve_user(self):
        token_response = self.client.post(
            reverse("users:token_obtain_pair"),
            {"email": self.user.email, "password": "testpassword"},
            format="json",
        )
        self.assertEqual(token_response.status_code, status.HTTP_200_OK)
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["email"], self.user.email)

    def test_update_book(self):

        update_payload = {
            "first_name": "Updated",
            "last_name": "User",
            "password": "newstrongpassword123",
        }
        response = self.client.patch(ME_URL, update_payload)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["first_name"], update_payload["first_name"])

        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password("newstrongpassword123"))
