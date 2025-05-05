from typing import Dict, List
import random

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from seeds import build_courses, build_students, build_enrollments, persist_entities
from school.models import Student, Course, Enrollment
from school.serializer import EnrollmentSerializer


class EnrollmentTestCase(APITestCase):
    def setUp(self) -> None:
        self.list_url = reverse('Enrollments-list')
        self.user = User.objects.create_superuser("admin")

        self.students: List[Student] = persist_entities(entities=build_students(total=200))
        self.courses: List[Course] = persist_entities(entities=build_courses(total=5))
        self.enrollments: List[Enrollment] = persist_entities(entities=build_enrollments(total=3))

    def test_list(self) -> None:
        """Verify if api can list entities"""
        self.client.force_authenticate(user=self.user)
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get(self) -> None:
        """Verify if HTTP GET is working"""
        self.client.force_authenticate(user=self.user)
        enrollments: List[Enrollment] = self.enrollments
        enrollment_01: Enrollment = random.sample(self.enrollments, 1)[0]
        enrollments.remove(enrollment_01)
        get_url: str = reverse('Enrollments-detail', kwargs={'pk': enrollment_01.id})
        resp = self.client.get(get_url, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

        enrollment_retrived: Enrollment = Enrollment.objects.filter(pk=resp.json()['id'])[0]
        self.assertEqual(enrollment_01.period, enrollment_retrived.period)
        self.assertEqual(enrollment_01.course, enrollment_retrived.course)
        self.assertEqual(enrollment_01.student, enrollment_retrived.student)

    def test_post(self) -> None:
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


class EnrollmentModelTestCase(TestCase):
    def setUp(self) -> None:
        self.students: List[Student] = persist_entities(entities=build_students(total=200))
        self.courses: List[Course] = persist_entities(entities=build_courses(total=5))
        self.enrollments: List[Enrollment] = persist_entities(entities=build_enrollments(total=3))

    def test_create(self) -> None:
        student: Student = build_students(total=1)[0]
        student.save()
        course: Course = build_courses(total=1)[0]
        course.save()

        enrollment: Enrollment = Enrollment(student=student, course=course, period=random.choice('MAN'))
        self.assertIsNone(enrollment.id)
        enrollment.save()
        self.assertIsNotNone(enrollment.id)


class EnrollmentSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.students: List[Student] = persist_entities(entities=build_students(total=20))
        self.courses: List[Course] = persist_entities(entities=build_courses(total=5))
        self.enrollments: List[Enrollment] = persist_entities(entities=build_enrollments(total=3))

        self.enrollment: Enrollment = random.sample(self.enrollments, 1)[0]
        self.serializer = EnrollmentSerializer(instance=self.enrollment)

    def test_serialized_fields(self) -> None:
        """Validate if is generating correct serialized data"""

        data: Dict = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'student', 'course', 'period']))
        self.assertEqual(data['id'], self.enrollment.id)
        self.assertEqual(data['student'], self.enrollment.student.id)
        self.assertEqual(data['course'], self.enrollment.course.id)
        self.assertEqual(data['period'], self.enrollment.period)

    def test_is_valid(self) -> None:
        valid_serializer: EnrollmentSerializer = EnrollmentSerializer(data=self.serializer.data)
        self.assertTrue(valid_serializer.is_valid())
        self.assertEqual(len(valid_serializer.errors), 0)

        invalid_data: Dict = {
            'student_id': random.sample(self.students, 1)[0],
            'course_id': random.sample(self.courses, 1)[0],
            'period': f'{random.choice("MAN")}'
        }
        invalid_serializer: EnrollmentSerializer = EnrollmentSerializer(data=invalid_data)
        self.assertFalse(invalid_serializer.is_valid())
