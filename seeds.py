import datetime
import json
import os
import random
from typing import Dict, List, Optional

import django
from django.core.serializers import serialize
from faker import Faker
from faker.providers import DynamicProvider
from validate_docbr import CPF

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'setup.settings')
django.setup()

from school.models import Course, Enrollment, Student


course_provider: DynamicProvider = DynamicProvider(provider_name='courses', elements=['Python Basic', 'Python Intermmediate', 'Python Advanced', 'Python Specialist', 'Python for Dummies'])
GENERATED_PREFIX: str = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')


def build_students(total: int) -> List[Student]:
    students: List[Student] = []
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
        students.append(student)

    return students


def build_courses(total: int) -> List[Course]:
    courses: List[Course] = []
    fake = Faker('pt_BR')
    fake.add_provider(course_provider)
    Faker.seed(10)
    for _ in range(total):
        course_code: str = f'{random.choice("ABCDEF")}{random.randrange(10, 99)}-{random.randrange(0, 9)}'
        description: str = fake.unique.courses()
        level: str = random.choice('BIE')
        course: Course = Course(course_code=course_code, description=description, level=level)
        courses.append(course)

    return courses


def build_enrollments(total: int, courses: Optional[List[Course]] = None, students: Optional[List[Student]] = None) -> List[Enrollment]:
    enrollments: List[Enrollment] = []
    if courses is None:
        courses: List[Course] = list(Course.objects.all())

    if students is None:
        students: List[Student] = list(Student.objects.all())

    for course in courses:
        sample_students: List[Student] = random.sample(students, total)
        for student in sample_students:
            students.remove(student)
            period: str = random.choice('MAN')  # see models.Enrollment.PERIOD
            enrollment: Enrollment = Enrollment(course=course, student=student, period=period)
            enrollments.append(enrollment)

    return enrollments


def persist_entities(entities: List) -> List:
    persisted_entities: List = []
    for entity in entities:
        entity.save()
        persisted_entities.append(entity)

    return persisted_entities


def save_fixtures(entities: List, filename: str) -> None:
    with open(filename, 'w') as f:
        serialized_data = json.loads(serialize('json', entities))
        for entity in serialized_data:
            entity['fields']['id'] = entity['pk']

        json.dump(serialized_data, f, indent=4)


if __name__ == "__main__":
    print('Creating students')
    students: List[Student] = persist_entities(entities=build_students(total=50))
    save_fixtures(entities=students, filename=f'school/fixtures/generated/{GENERATED_PREFIX}_students.json')

    print('Creating courses')
    courses: List[Course] = persist_entities(entities=build_courses(total=5))
    save_fixtures(entities=courses, filename=f'school/fixtures/generated/{GENERATED_PREFIX}_courses.json')

    print('Creating Enrollments with dependencies')
    enrollments: List[Enrollment] = persist_entities(entities=build_enrollments(total=3))
    save_fixtures(entities=enrollments, filename=f'school/fixtures/generated/{GENERATED_PREFIX}_enrollments.json')
