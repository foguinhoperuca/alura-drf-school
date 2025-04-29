from typing import List
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school.models import Course
from seeds import build_courses, persist_entities


class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        self.list_url = reverse('Courses-list')
        print('Creating courses')
        self.entities: List[Course] = persist_entities(entities=build_courses(total=5))

    # def test_fail(self) -> None:
    #     self.fail('Failed - Just a controlled test')

    def test_list(self) -> None:
        """Verify if HTTP GET is working"""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.entities), len(resp.json()))
