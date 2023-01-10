from rest_framework.viewsets import ModelViewSet
from school.models import Student, Course
from school.serializer import StudentSerializer, CourseSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
