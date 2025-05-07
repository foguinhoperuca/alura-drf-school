from enum import Enum

from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=128)
    rg = models.CharField(max_length=16)
    cpf = models.CharField(max_length=16)
    birthday = models.DateField()
    mobile = models.CharField(max_length=32, default="")
    photo = models.ImageField(null=True, blank=True)
    email = models.EmailField(max_length=32, null=True, blank=False)

    def __str__(self):
        return f'{self.name} RG {self.rg} CPF {self.cpf} birthday {self.birthday}'


class Course(models.Model):
    class Level(Enum):
        BASIC = 'Básico'
        INTERMEDIARY = 'Intermediário'
        EXPERT = 'Avançado'

    course_code = models.CharField(max_length=8)
    description = models.CharField(max_length=128, blank=False)
    level = models.CharField(max_length=16, choices=tuple((e.name, e.value) for e in Level), blank=False, null=False, default=Level.BASIC.name)

    def __str__(self):
        return f'#{self.course_code} [{self.level}] {self.description}'


class Enrollment(models.Model):
    class Period(Enum):
        MORNING = 'Matutino'
        AFTERNOON = 'Vespertino'
        NIGHT = 'Noturno'

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    period = models.CharField(max_length=16, choices=tuple((e.name, e.value) for e in Period), blank=False, null=False, default=Period.MORNING.name)

    def __str__(self):
        return f'[{self.id}] Student {self.student} is enrolled in course {self.course} in period {Enrollment.Period[self.period].value}'
