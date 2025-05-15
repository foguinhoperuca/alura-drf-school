from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ModelViewSet

from django.utils.translation import get_language
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.throttling import UserRateThrottle

from school.models import Student, Course, Enrollment
from school.permissions import StrictDjangoModelPermissions
from school.serializer import CourseSerializer, EnrollmentSerializer, ListEnrollmentsStudentsSerializer, ListCoursesEnrollmentsSerializer, StudentSerializer, StudentSerializerV2, StudentSerializerV3, StudentSerializerV4
from school.throttles import CourseAnonRateThrottle


class StudentViewSet(ModelViewSet):
    """
    Endpoint of student's CRUD.

    Description of ViewSet:
    - Ordering by name (default) and birthday
    - Search by cpf, rg and name
    - Allowed methods: full CRUD REST

    Serializer and version implementation:
    - version = [v1 | v2 | v3 | v4]. Default v4.
    - v1: Basic data
    - v2: added mobile
    - v3: added photo
    - v4: added email
    """
    queryset = Student.objects.all().order_by('name')
    permission_classes = [IsAuthenticated, StrictDjangoModelPermissions]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['name', 'birthday']
    search_fields = ['cpf', 'rg', 'name']

    def get_serializer_class(self):
        # TODO implement log file
        # print(f"version of student's api is: {self.request.version}")

        if self.request.version is not None:
            if self.request.version.lower() == 'v1':
                return StudentSerializer
            elif self.request.version.lower() == 'v2':
                return StudentSerializerV2
            elif self.request.version.lower() == 'v3':
                return StudentSerializerV3
            elif self.request.version.lower() == 'v4':
                return StudentSerializerV4

        return StudentSerializerV4


class CourseViewSet(ModelViewSet):
    """
    API without auth. Only GET is allowed.

    Throttle Classes:
    - CourseAnonRateThrottle: limit responses for anonymous user. Default 5/hour. Global default is 150/day.

    """

    queryset = Course.objects.all().order_by('course_code')
    serializer_class = CourseSerializer
    permission_classes = []
    http_method_names = ['get']
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['level']
    search_fields = ['course_code']
    throttle_classes = [CourseAnonRateThrottle]

    def get(self, request):
        print("Idioma ativo:", get_language())

        return Response({'mensagem': 'Teste de idioma'})


class EnrollmentViewSet(ModelViewSet):
    """
    Endpoint for enrollment's CRUD.

    Description of ModelViewSet:
    - Only authenticated can acess

    Throttle Classes:
    - UserRateThrottle: limit responses for authenticated users. Default is 30/minute.
    """
    queryset = Enrollment.objects.all().order_by('course__id')
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    ordering_fields = ['period', 'course__course_code']
    search_fields = ['course__course_code']
    throttle_classes = [UserRateThrottle]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            serializer.save()
            response = Response(serializer.data, status=HTTP_201_CREATED)
            response['Location'] = request.build_absolute_uri() + str(serializer.data['id'])
        else:
            response = Response(f'Invalid Data! {serializer.errors}', status=HTTP_500_INTERNAL_SERVER_ERROR)

        return response

    @method_decorator(cache_page(20))
    def dispatch(self, *args, **kwargs):
        return super(EnrollmentViewSet, self).dispatch(*args, **kwargs)


class ListEnrollmentsStudents(ListAPIView):
    """
    Endpoint to get enrollments by student.

    Parameters used:
    - pk (int): identification for object. Must be an integer.
    """
    serializer_class = ListEnrollmentsStudentsSerializer

    def get_queryset(self):
        # code just for schema generation metadata
        if getattr(self, 'swagger_fake_view', False):
            return Enrollment.objects.none()

        return Enrollment.objects.filter(student_id=self.kwargs['pk']).order_by('id')


class ListCoursesEnrollments(ListAPIView):
    """
    Endpoint to get enrollments by course.

    Parameters used:
    - pk (int): identification for object. Must be an integer.
    """
    serializer_class = ListCoursesEnrollmentsSerializer

    def get_queryset(self):
        # code just for schema generation metadata
        if getattr(self, 'swagger_fake_view', False):
            return Enrollment.objects.none()

        return Enrollment.objects.filter(course_id=self.kwargs['pk']).order_by('id')
