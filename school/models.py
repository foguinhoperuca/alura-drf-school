from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=30)
    rg = models.CharField(max_length=9)
    cpf = models.CharField(max_length=11)
    birthday = models.DateField()

    def __str__(self):
        return f'{self.name} RG {self.rg} CPF {self.cpf} birthday {self.birthday}'


class Course(models.Model):
    LEVEL = (
        ('B', 'Basic'),
        ('I', 'Intermediary'),
        ('E', 'Expert')
    )
    course_code = models.CharField(max_length=10)
    description = models.CharField(max_length=100)
    level = models.CharField(max_length=1, choices=LEVEL, blank=False, null=False, default='B')

    def __str__(self):
        return f'#{self.course_code} [{self.level}] {self.description}'
