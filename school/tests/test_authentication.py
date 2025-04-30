from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationUserTestCase(APITestCase):
    def setUp(self) -> None:
        self.list_url: str = reverse('Enrollments-list')
        self.user: User = User.objects.create_user('admin', password='A12345678a')

    def test_auth_user(self) -> None:
        """Test all kind of authentication: correct, not authorized, wrong username, wrong password, get resource from api when authenticated."""

        user: User = authenticate(username='admin', password='A12345678a')
        self.assertTrue((user is not None) and user.is_authenticated)
