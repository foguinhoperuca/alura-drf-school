from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationUserTestCase(APITestCase):
    def setUp(self) -> None:
        self.list_url: str = reverse('Enrollments-list')
        self.user: User = User.objects.create_user('admin', password='A12345678a')

    def test_authentication(self) -> None:
        """Test all kind of authentication: wrong username, wrong password, get resource from api when authenticated."""

        user: User = authenticate(username='admin', password='A12345678a')
        self.assertTrue((user is not None) and user.is_authenticated)

        user_not_auth: User = authenticate(username='admin', password='XPTO')
        self.assertFalse((user_not_auth is not None) and user_not_auth.is_authenticated)

        username_unknow: User = authenticate(username='unknow', password='A12345678a')
        self.assertFalse((username_unknow is not None) and username_unknow.is_authenticated)

    def test_authorization(self) -> None:
        """Test authorization access in api."""

        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(self.user)
        self.assertEqual(self.client.get(self.list_url).status_code, status.HTTP_200_OK)
