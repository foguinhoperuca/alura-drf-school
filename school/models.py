from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=30)
    rg = models.CharField(max_length=9)
    cpf = models.CharField(max_length=11)
    birthday = models.DateField()
    mobile = models.CharField(max_length=32, default="")
    photo = models.ImageField(null=True, blank=True)

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


class Enrollment(models.Model):
    PERIOD = (
        ('M', 'Morning'),
        ('A', 'Afternoon'),
        ('N', 'Night')
    )
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    period = models.CharField(max_length=1, choices=PERIOD, blank=False, null=False, default='M')

    def __str__(self):
        return f'[{self.id}] Student {self.student} is enrolled in course {self.course} in period {[per[1] for per in Enrollment.PERIOD if per[0] == self.period][0]}'
