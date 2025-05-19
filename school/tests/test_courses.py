import random
from typing import Dict, List

from django.test import TestCase
from django.urls import reverse
from faker import Faker
from faker.providers import DynamicProvider
from rest_framework import status
from rest_framework.test import APITestCase

from school.models import Course
from school.serializer import CourseSerializer
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
        self.assertEqual(len(self.entities), len(resp.json()['results']))


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


class CourseSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.entities: List[Course] = persist_entities(entities=build_courses(total=5))

        self.entity: Course = random.sample(self.entities, 1)[0]
        self.serializer = CourseSerializer(instance=self.entity)

    def test_serialized_fields(self) -> None:
        """Validate if is generating correct serialized data"""

        data: Dict = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'course_code', 'description', 'level']))
        self.assertEqual(data['id'], self.entity.id)
        self.assertEqual(data['course_code'], self.entity.course_code)
        self.assertEqual(data['description'], self.entity.description)
        self.assertEqual(data['level'], self.entity.level)

    def test_is_valid(self) -> None:
        fake: Faker = Faker('pt_BR')
        Faker.seed(62)
        fake.add_provider(DynamicProvider(provider_name='courses', elements=['Python Basic', 'Python Intermmediate', 'Python Advanced', 'Python Specialist', 'Python for Dummies']))
        valid_data: Dict = {
            'course_code': f'{random.choice("ABCDEF")}{random.randrange(10, 99)}-{random.randrange(0, 9)}',
            'description': fake.unique.courses(),
            'level': random.choice([e.name for e in Course.Level]),
        }
        valid_serializer: CourseSerializer = CourseSerializer(data=valid_data)
        self.assertTrue(valid_serializer.is_valid())
        self.assertEqual(len(valid_serializer.errors), 0)

        invalid_data = {
            'course_code': f'{random.choice("ABCDEF")}{random.randrange(10, 99)}-{random.randrange(0, 9)}'[0:2],
            'description': fake.unique.courses(),
            'level': random.choice([e.name for e in Course.Level]),
        }
        invalid_serializer: CourseSerializer = CourseSerializer(data=invalid_data)
        self.assertFalse(invalid_serializer.is_valid())
        self.assertEqual(len(invalid_serializer.errors), 1)
        self.assertEqual(invalid_serializer.errors['course_code'][0].code, 'min_length')

        invalid_data = {
            'course_code': f'{random.randrange(0, 9)}{random.choice("ABCDEF")}{random.randrange(10, 99)}-{random.randrange(0, 9)}',
            'description': fake.unique.courses(),
            'level': random.choice([e.name for e in Course.Level]),
        }
        invalid_serializer: CourseSerializer = CourseSerializer(data=invalid_data)
        self.assertFalse(invalid_serializer.is_valid())
        self.assertEqual(len(invalid_serializer.errors), 1)
        self.assertEqual(invalid_serializer.errors['course_code'][0].code, 'invalid')
