from enum import Enum

from django.core.validators import MinLengthValidator
from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=128, verbose_name='Name', validators=[MinLengthValidator(3)])
    rg = models.CharField(max_length=16, verbose_name='RG')
    cpf = models.CharField(max_length=16, verbose_name='CPF', unique=True)
    birthday = models.DateField(verbose_name='BDay')
    mobile = models.CharField(max_length=32, default="", verbose_name='Mobile')
    photo = models.ImageField(null=True, blank=True, verbose_name='Photo')
    email = models.EmailField(max_length=32, null=True, blank=False, verbose_name='E-mail', validators=[MinLengthValidator(13)])

    class Meta:
        verbose_name = 'Student'
        verbose_name_plural = 'Students'

    def __str__(self):
        return f'{self.name} RG {self.rg} CPF {self.cpf} birthday {self.birthday}'


class Course(models.Model):
    class Level(Enum):
        BASIC = 'Básico'
        INTERMEDIARY = 'Intermediário'
        EXPERT = 'Avançado'

    course_code = models.CharField(max_length=8, unique=True, validators=[MinLengthValidator(3)], verbose_name='Code')
    description = models.CharField(max_length=128, blank=False, verbose_name='Description')
    level = models.CharField(max_length=16, choices=tuple((e.name, e.value) for e in Level), blank=False, null=False, default=Level.BASIC.name, verbose_name='Level')

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f'#{self.course_code} [{self.level}] {self.description}'


class Enrollment(models.Model):
    class Period(Enum):
        MORNING = 'Matutino'
        AFTERNOON = 'Vespertino'
        NIGHT = 'Noturno'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, verbose_name='Student')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Course')
    period = models.CharField(max_length=16, choices=tuple((e.name, e.value) for e in Period), blank=False, null=False, default=Period.MORNING.name, verbose_name='Period')

    class Meta:
        verbose_name = 'Enrollment'
        verbose_name_plural = 'Enrollments'

    def __str__(self):
        return f'[{self.id}] Student {self.student} is enrolled in course {self.course} in period {Enrollment.Period[self.period].value}'
