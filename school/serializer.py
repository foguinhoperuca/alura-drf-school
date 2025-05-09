import re
from typing import Any, Dict

from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField, ValidationError
from school.models import Student, Course, Enrollment
from school.validators import validate_allowed_period


class CustomStudentValidation:
    def validate_name(self, name: str) -> str:
        if not name.isalpha():
            raise ValidationError('Name must be alpha!! Len should be more than 3!!')

        return name


class StudentSerializer(ModelSerializer, CustomStudentValidation):
    class Meta:
        model = Student
        fields = ['id', 'name', 'rg', 'cpf', 'birthday']


class StudentSerializerV2(ModelSerializer, CustomStudentValidation):
    class Meta:
        model = Student
        fields = ['id', 'name', 'rg', 'cpf', 'birthday', 'mobile']


class StudentSerializerV3(ModelSerializer, CustomStudentValidation):
    class Meta:
        model = Student
        fields = ['id', 'name', 'rg', 'cpf', 'birthday', 'mobile', 'photo']


class StudentSerializerV4(ModelSerializer, CustomStudentValidation):
    class Meta:
        model = Student
        fields = ['id', 'name', 'rg', 'cpf', 'birthday', 'mobile', 'photo', 'email']


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate_course_code(self, course_code: str) -> str:
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9-]*$', course_code):
            raise ValidationError('Course code must start with an Letter!! It can have numbers and hypen. Should be 3 or more characters.')

        return course_code


class EnrollmentSerializer(ModelSerializer):
    class Meta:
        model = Enrollment
        exclude = []


class ListEnrollmentsStudentsSerializer(ModelSerializer):
    course = ReadOnlyField(source='course.description')
    period = SerializerMethodField()
    student = ReadOnlyField(source='student.name')

    class Meta:
        model = Enrollment
        fields = ['course', 'period', 'student']

    def get_period(self, obj):
        # FIXME where come from get_period_display
        return obj.get_period_display()

    def validate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # TODO test it! Review if choices are already validating!
        if not validate_allowed_period(data['period']):
            raise ValidationError('Period {data["period"]} is invalid!!')

        return data


class ListCoursesEnrollmentsSerializer(ModelSerializer):
    course = ReadOnlyField(source='course.description')
    student_id = ReadOnlyField(source='student.id')
    student_name = ReadOnlyField(source='student.name')
    student_cpf = ReadOnlyField(source='student.cpf')
    student_rg = ReadOnlyField(source='student.rg')
    student_birthday = ReadOnlyField(source='student.birthday')
    student_mobile = ReadOnlyField(source='student.mobile')
    student_email = ReadOnlyField(source='student.email')

    class Meta:
        model = Enrollment
        fields = ['course', 'student_id', 'student_name', 'student_cpf', 'student_rg', 'student_birthday', 'student_mobile', 'student_email']
