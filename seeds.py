import datetime
import os
import random
from typing import List

import django
from faker import Faker
from faker.providers import DynamicProvider
from validate_docbr import CPF

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from school.models import Course, Enrollment, Student


course_provider: DynamicProvider = DynamicProvider(provider_name='courses', elements=['Python Basic', 'Python Intermmediate', 'Python Advanced', 'Python Specialist', 'Python for Dummies'])

def create_students(total: int) -> None:
    fake = Faker('pt_BR')
    Faker.seed(10)
    for _ in range(total):
        cpf: CPF = CPF()
        name: str = fake.name()
        rg: str = f'{random.randrange(10, 99)}{random.randrange(100, 999)}{random.randrange(100, 999)}{random.randrange(0, 9)}'
        cpf_number: str = cpf.generate()
        birthday: datetime.datetime = fake.date_between(start_date='-18y', end_date='today')
        mobile: str = fake.phone_number()
        student: Student = Student(name=name, rg=rg, cpf=cpf_number, birthday=birthday, mobile=mobile)
        student.save()

def create_courses(total: int) -> None:
    fake = Faker('pt_BR')
    fake.add_provider(course_provider)
    Faker.seed(10)
    for _ in range(total):
        course_code: str = f'{random.choice("ABCDEF")}{random.randrange(10, 99)}-{random.randrange(0, 9)}'
        description: str = fake.unique.courses()
        level: str = random.choice('BIE')
        course: Course = Course(course_code=course_code, description=description, level=level)
        course.save()

create_students(200)
create_courses(5)
