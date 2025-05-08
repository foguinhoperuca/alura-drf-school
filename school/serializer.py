from rest_framework.serializers import ModelSerializer, ReadOnlyField, SerializerMethodField
from school.models import Student, Course, Enrollment


class StudentSerializer(ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'rg', 'cpf', 'birthday']


class StudentSerializerV2(ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'rg', 'cpf', 'birthday', 'mobile']


class StudentSerializerV3(ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'rg', 'cpf', 'birthday', 'mobile', 'photo']


class StudentSerializerV4(ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'rg', 'cpf', 'birthday', 'mobile', 'photo', 'email']


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class EnrollmentSerializer(ModelSerializer):
    class Meta:
        model = Enrollment
        exclude = []


class ListEnrollmentsStudentsSerializer(ModelSerializer):
    course = ReadOnlyField(source='course.description')
    period = SerializerMethodField()
    student = ReadOnlyField(source='student.name')

    class Meta:
        model = Enrollment
        fields = ['course', 'period', 'student']

    def get_period(self, obj):
        # FIXME where come from get_period_display
        return obj.get_period_display()


class ListCoursesEnrollmentsSerializer(ModelSerializer):
    course = ReadOnlyField(source='course.description')
    student_id = ReadOnlyField(source='student.id')
    student_name = ReadOnlyField(source='student.name')
    student_cpf = ReadOnlyField(source='student.cpf')
    student_rg = ReadOnlyField(source='student.rg')
    student_birthday = ReadOnlyField(source='student.birthday')
    student_mobile = ReadOnlyField(source='student.mobile')
    student_email = ReadOnlyField(source='student.email')

    class Meta:
        model = Enrollment
        fields = ['course', 'student_id', 'student_name', 'student_cpf', 'student_rg', 'student_birthday', 'student_mobile', 'student_email']
