from typing import List

from django.test import TestCase
from django.urls import reverse
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from school.models import Course
from seeds import build_courses, persist_entities


class CourseTestCase(APITestCase):
    def setUp(self) -> None:
        self.list_url = reverse('Courses-list')
        self.entities: List[Course] = persist_entities(entities=build_courses(total=5))

    # def test_fail(self) -> None:
    #     self.fail('Failed - Just a controlled test')

    def test_list(self) -> None:
        """Verify if HTTP GET is working"""
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(self.entities), len(resp.json()))


class CourseFixturesTestCase(TestCase):
    fixtures = ['courses']

    def test_fixtures(self):
        courses = Course.objects.all()
        self.assertEqual(len(courses), 5)
        for course in courses:
            self.assertTrue(course.id in [16, 17, 18, 19, 20])


class CourseModelTestCase(TestCase):
    def setUp(self) -> None:
        self.entities: List[Course] = persist_entities(entities=build_courses(total=5))

    def test_update(self) -> None:
        fake = Faker('pt_BR')
        Faker.seed(99)
        course_01: Course = Course.objects.get(pk=1)
        course_control: Course = Course.objects.get(pk=1)
        course_01.description = fake.sentence()
        course_01.save()

        course_from_db: Course = Course.objects.get(pk=1)
        self.assertEqual(course_01.description, course_from_db.description)
        self.assertNotEqual(course_control.description, course_from_db.description)
