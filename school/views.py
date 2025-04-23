from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions

from school.permissions import StrictDjangoModelPermissions
from school.models import Student, Course, Enrollment
from school.serializer import StudentSerializer, StudentSerializerV2, CourseSerializer, EnrollmentSerializer, ListEnrollmentsStudentsSerializer, ListStudentsEnrollmentsSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return StudentSerializerV2
        else:
            return StudentSerializer


# API without auth
class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = []
    http_method_names = ['get']


class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer


class ListEnrollmentsStudents(ListAPIView):
    serializer_class = ListEnrollmentsStudentsSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student_id=self.kwargs['pk'])


class ListStudentsEnrollments(ListAPIView):
    serializer_class = ListStudentsEnrollmentsSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(course_id=self.kwargs['pk'])

