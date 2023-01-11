from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from school.models import Student, Course, Enrollment
from school.serializer import StudentSerializer, CourseSerializer, EnrollmentSerializer, ListEnrollmentsStudentsSerializer, ListStudentsEnrollmentsSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    # API without auth


class EnrollmentViewSet(ModelViewSet):
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ListEnrollmentsStudents(ListAPIView):
    def get_queryset(self):
        return Enrollment.objects.filter(student_id=self.kwargs['pk'])

    serializer_class = ListEnrollmentsStudentsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ListStudentsEnrollments(ListAPIView):
    def get_queryset(self):
        return Enrollment.objects.filter(course_id=self.kwargs['pk'])

    serializer_class = ListStudentsEnrollmentsSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]
