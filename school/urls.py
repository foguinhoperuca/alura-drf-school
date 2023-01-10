from django.urls import path, include
from rest_framework.routers import DefaultRouter
from school.views import StudentViewSet, CourseViewSet, EnrollmentViewSet

router = DefaultRouter()
router.register('students', StudentViewSet, basename='Students')
router.register('courses', CourseViewSet, basename='Courses')
router.register('enrollments', EnrollmentViewSet, basename='Enrollments')

urlpatterns = [
    path('', include(router.urls)),
]
