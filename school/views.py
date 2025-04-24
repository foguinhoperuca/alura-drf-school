from rest_framework.authentication import BasicAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.viewsets import ModelViewSet

from school.models import Student, Course, Enrollment
from school.permissions import StrictDjangoModelPermissions
from school.serializer import StudentSerializer, StudentSerializerV2, StudentSerializerV3, CourseSerializer, EnrollmentSerializer, ListEnrollmentsStudentsSerializer, ListStudentsEnrollmentsSerializer


class StudentViewSet(ModelViewSet):
    queryset = Student.objects.all()
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return StudentSerializerV2
        elif self.request.version == 'v3':
            return StudentSerializerV3
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

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=HTTP_201_CREATED)
            response['Location'] = request.build_absolute_uri() + str(serializer.data['id'])

            return response


class ListEnrollmentsStudents(ListAPIView):
    serializer_class = ListEnrollmentsStudentsSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(student_id=self.kwargs['pk'])


class ListStudentsEnrollments(ListAPIView):
    serializer_class = ListStudentsEnrollmentsSerializer

    def get_queryset(self):
        return Enrollment.objects.filter(course_id=self.kwargs['pk'])
