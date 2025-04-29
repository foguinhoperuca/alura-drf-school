from typing import List
import random

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from school.models import Student, Course, Enrollment
from seeds import build_courses, build_students, build_enrollments, persist_entities


class EnrollmentTestCase(APITestCase):
    def setUp(self) -> None:
        self.list_url = reverse('Enrollments-list')
        self.user = User.objects.create_superuser("admin")

        print('Creating students')
        self.students: List[Student] = persist_entities(entities=build_students(total=200))
        print('Creating courses')
        self.courses: List[Course] = persist_entities(entities=build_courses(total=5))
        print('Creating Enrollments with dependencies')
        self.enrollments: List[Enrollment] = persist_entities(entities=build_enrollments(total=3))

    def test_list(self) -> None:
        """Verify if HTTP GET is working"""
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_save(self) -> None:
        """Verify if saving is working"""

        enrollments: List[Enrollment] = self.enrollments
        enrollment_01: Enrollment = random.sample(self.enrollments, 1)[0]
        enrollments.remove(enrollment_01)
        enrollment_02: Enrollment = random.sample(self.enrollments, 1)[0]
        enrollments.remove(enrollment_02)
        data = {
            'student_id': enrollment_01.student.id,
            'course_id': enrollment_02.course.id,
            'period': random.choice('MAN')
        }

        self.client.force_authenticate(user=self.user)
        resp = self.client.post(self.list_url, data=data, format='json')
        breakpoint()
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        breakpoint()
        enrollment_persisted: Enrollment = Enrollment.objects.find(resp.json()['id'])
        self.assertNotNone(enrollment_persisted)
