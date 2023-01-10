from rest_framework.serializers import ModelSerializer
from school.models import Student, Course, Enrollment


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'rg', 'cpf', 'birthday']


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class EnrollmentSerializer(ModelSerializer):
    class Meta:
        model = Enrollment
        exclude = []