from django.urls import path, include

from rest_framework.routers import DefaultRouter

from school.views import StudentViewSet, CourseViewSet, EnrollmentViewSet, ListEnrollmentsStudents, ListStudentsEnrollments

router = DefaultRouter()
router.register('students', StudentViewSet, basename='Students')
router.register('courses', CourseViewSet, basename='Courses')
router.register('enrollments', EnrollmentViewSet, basename='Enrollments')

urlpatterns = [
    path('', include(router.urls)),
    path('students/<int:pk>/enrollments/', ListEnrollmentsStudents.as_view()),
    path('courses/<int:pk>/enrollments/', ListStudentsEnrollments.as_view())
]
