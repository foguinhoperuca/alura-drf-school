from django.contrib import admin
from school.models import Student, Course, Enrollment


class Students(admin.ModelAdmin):
    list_display = ('id', 'name', 'rg', 'cpf', 'birthday')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_per_page = 10


class Courses(admin.ModelAdmin):
    list_display = ('id', 'course_code', 'description')
    list_display_links = ('id', 'course_code')
    search_fields = ('course_code',)


class Enrollments(admin.ModelAdmin):
    list_display = ('id', 'student', 'course', 'period')
    list_display_links = ('id', 'student', 'course')
    search_fields = ('period',)


admin.site.register(Student, Students)
admin.site.register(Course, Courses)
admin.site.register(Enrollment, Enrollments)
