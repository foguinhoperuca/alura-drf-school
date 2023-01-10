from django.urls import path
from school.views import students

urlpatterns = [
    path('', students, name='students'),
]
