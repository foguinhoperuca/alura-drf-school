from typing import List

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school.models import Student
from seeds import build_students, persist_entities


class StudentTestCase(APITestCase):
    def setUp(self) -> None:
        self.list_url = reverse('Students-list')
        self.user = User.objects.create_superuser("admin")
        self.students: List[Student] = persist_entities(entities=build_students(total=5))

    def test_list(self) -> None:
        """Verify if HTTP GET is working"""
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.students), len(resp.json()))
