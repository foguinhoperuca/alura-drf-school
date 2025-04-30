from typing import Dict, List
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

        self.client.force_authenticate(user=self.user)
        enrollments: List[Enrollment] = self.enrollments
        enrollment_01: Enrollment = random.sample(self.enrollments, 1)[0]
        enrollments.remove(enrollment_01)
        enrollment_02: Enrollment = random.sample(self.enrollments, 1)[0]
        enrollments.remove(enrollment_02)

        data = {
            'student': enrollment_01.student.id,
            'course': enrollment_02.course.id,
            'period': random.choice('MAN')
        }
        resp = self.client.post(self.list_url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        enrollment_persisted: Enrollment = Enrollment.objects.filter(pk=resp.json()['id'])[0]
        self.assertIsNotNone(enrollment_persisted)

        data['student_id'] = data['student']
        del data['student']
        resp = self.client.post(self.list_url, data=data, format='json')
        self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    def test_put(self) -> None:
        """Verify update"""

        self.client.force_authenticate(user=self.user)

        enrollments: List[Enrollment] = self.enrollments
        enrollment_01: Enrollment = random.sample(self.enrollments, 1)[0]
        enrollments.remove(enrollment_01)
        period_old: str = enrollment_01.period
        update_url = reverse('Enrollments-detail', kwargs={'pk': enrollment_01.id})

        periods: List = [e[0] for e in Enrollment.PERIOD]
        periods.remove(enrollment_01.period)
        period_update: str = random.sample(periods, 1)[0]

        data: Dict = {
            'id': enrollment_01.id,
            'student': enrollment_01.student.id,
            'course': enrollment_01.course.id,
            'period': period_update
        }
        resp = self.client.put(update_url, data=data, format='json')

        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        enrollment_persisted: Enrollment = Enrollment.objects.filter(pk=resp.json()['id'])[0]
        self.assertIsNotNone(enrollment_persisted)
        self.assertEqual(enrollment_01.id, enrollment_persisted.id)
        self.assertEqual(enrollment_persisted.period, period_update)
        self.assertNotEqual(enrollment_persisted.period, period_old)

    def test_delete(self) -> None:
        enrollments: List[Enrollment] = self.enrollments
        enrollment_01: Enrollment = random.sample(self.enrollments, 1)[0]
        enrollments.remove(enrollment_01)
        delete_url = reverse('Enrollments-detail', kwargs={'pk': enrollment_01.id})

        resp = self.client.delete(delete_url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)

        self.client.force_authenticate(user=self.user)
        resp = self.client.delete(delete_url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        enrollment_persisted: Enrollment = Enrollment.objects.filter(pk=enrollment_01.id)
        self.assertEqual(len(list(enrollment_persisted)), 0)
