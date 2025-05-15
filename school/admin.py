from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin, GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group

from unfold.admin import ModelAdmin
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm

from school.models import Student, Course, Enrollment


admin.site.unregister(User)
admin.site.unregister(Group)


class Students(ModelAdmin):
    list_display = ('id', 'name', 'rg', 'cpf', 'birthday', 'mobile', 'email', 'photo',)
    list_display_links = ('id', 'name', 'cpf', 'birthday', 'mobile', 'email', 'photo',)
    search_fields = ('name', 'cpf', 'rg', 'mobile')
    list_per_page = 25
    ordering = ('id', 'name', 'birthday')


class Courses(ModelAdmin):
    list_display = ('id', 'course_code', 'description')
    list_display_links = ('id', 'course_code')
    search_fields = ('course_code',)
    ordering = ('id', 'course_code')


class Enrollments(ModelAdmin):
    list_display = ('id', 'student', 'course', 'period')
    list_display_links = ('id', 'student', 'course')
    search_fields = ('period',)
    ordering = ('id', 'period')


@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass


admin.site.register(Student, Students)
admin.site.register(Course, Courses)
admin.site.register(Enrollment, Enrollments)
