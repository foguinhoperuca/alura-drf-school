import random
from typing import Dict, List

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from faker import Faker
from rest_framework import status
from rest_framework.test import APITestCase

from school.models import Student
from school.serializer import StudentSerializer, StudentSerializerV2, StudentSerializerV3, StudentSerializerV4
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


class StudentModelTestCase(TestCase):
    def setUp(self) -> None:
        self.students: List[Student] = persist_entities(entities=build_students(total=200))

    def test_create(self) -> None:
        student: Student = build_students(total=1)[0]
        self.assertIsNone(student.id)
        student.save()
        self.assertIsNotNone(student.id)
        self.assertEqual(student.id, 201)

    def test_update(self) -> None:
        fake: Faker = Faker('pt_BR')
        Faker.seed(99)
        student_01: Student = Student.objects.get(pk=1)
        student_control: Student = Student.objects.get(pk=1)
        student_01.name = fake.name()
        student_01.save()

        student_from_db: Student = Student.objects.get(pk=1)
        self.assertEqual(student_01.name, student_from_db.name)
        self.assertNotEqual(student_control.name, student_from_db.name)


class StudentSerializerTestCase(TestCase):
    def setUp(self) -> None:
        self.entities: List[Student] = persist_entities(entities=build_students(total=20))

        self.entity: Student = random.sample(self.entities, 1)[0]
        self.serializer = StudentSerializer(instance=self.entity)
        self.serializerv2 = StudentSerializerV2(instance=self.entity)
        self.serializerv3 = StudentSerializerV3(instance=self.entity)
        self.serializerv4 = StudentSerializerV4(instance=self.entity)

    def test_serialized_fields(self) -> None:
        """Validate if is generating correct serialized data"""

        data: Dict = self.serializer.data
        self.assertEqual(set(data.keys()), set(['id', 'name', 'rg', 'cpf', 'birthday']))
        self.assertFalse('mobile' in set(data.keys()))
        self.assertFalse('photo' in set(data.keys()))
        self.assertFalse('email' in set(data.keys()))
        self.assertEqual(data['id'], self.entity.id)
        self.assertEqual(data['name'], self.entity.name)
        self.assertEqual(data['rg'], self.entity.rg)
        self.assertEqual(data['cpf'], self.entity.cpf)
        self.assertEqual(data['birthday'], self.entity.birthday.strftime('%Y-%m-%d'))

        datav2: Dict = self.serializerv2.data
        self.assertEqual(set(datav2.keys()), set(['id', 'name', 'rg', 'cpf', 'birthday', 'mobile']))
        self.assertFalse('photo' in set(datav2.keys()))
        self.assertFalse('email' in set(datav2.keys()))
        self.assertEqual(datav2['id'], self.entity.id)
        self.assertEqual(datav2['name'], self.entity.name)
        self.assertEqual(datav2['rg'], self.entity.rg)
        self.assertEqual(datav2['cpf'], self.entity.cpf)
        self.assertEqual(datav2['birthday'], self.entity.birthday.strftime('%Y-%m-%d'))
        self.assertEqual(datav2['mobile'], self.entity.mobile)

        datav3: Dict = self.serializerv3.data
        self.assertEqual(set(datav3.keys()), set(['id', 'name', 'rg', 'cpf', 'birthday', 'mobile', 'photo']))
        self.assertFalse('email' in set(datav3.keys()))
        self.assertEqual(datav3['id'], self.entity.id)
        self.assertEqual(datav3['name'], self.entity.name)
        self.assertEqual(datav3['rg'], self.entity.rg)
        self.assertEqual(datav3['cpf'], self.entity.cpf)
        self.assertEqual(datav3['birthday'], self.entity.birthday.strftime('%Y-%m-%d'))
        self.assertEqual(datav3['mobile'], self.entity.mobile)
        self.assertEqual(datav3['photo'], self.entity.photo)

        datav4: Dict = self.serializerv4.data
        self.assertEqual(set(datav4.keys()), set(['id', 'name', 'rg', 'cpf', 'birthday', 'mobile', 'photo', 'email']))
        self.assertEqual(datav4['id'], self.entity.id)
        self.assertEqual(datav4['name'], self.entity.name)
        self.assertEqual(datav4['rg'], self.entity.rg)
        self.assertEqual(datav4['cpf'], self.entity.cpf)
        self.assertEqual(datav4['birthday'], self.entity.birthday.strftime('%Y-%m-%d'))
        self.assertEqual(datav4['mobile'], self.entity.mobile)
        self.assertEqual(datav4['photo'], self.entity.photo)
        self.assertEqual(datav4['email'], self.entity.mobile)

    def test_is_valid(self) -> None:
        valid_serializer: StudentSerializer = StudentSerializer(data=self.serializer.data)
        self.assertTrue(valid_serializer.is_valid())
        self.assertEqual(len(valid_serializer.errors), 0)

        # # Models
        # ## name min lenght 3
        # ## cpf unique
        # ## email min lenght 3
        # # Serializer
        # ## validate_name
        # ## validate cpf

        fake: Faker = Faker('pt_BR')
        Faker.seed(76)
        invalid_data: Dict = {
            'name': fake.name(),
            'rg': '',
            'cpf': f'{random.choice("MAN")}',
            'birthday': fake.date_between(start_date='-35y', end_date='today'),
            'mobile': '',
            'photo': '',
            'email': ''
        }
        invalid_serializer: StudentSerializer = StudentSerializer(data=invalid_data)
        self.assertFalse(invalid_serializer.is_valid())
