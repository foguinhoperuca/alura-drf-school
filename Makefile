test-enrollment:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments
	@date

test-enrollment-model:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments.EnrollmentModelTestCase
	@date

test-enrollment-model-create:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments.EnrollmentModelTestCase.test_create
	@date

test-enrollment-serializer:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments.EnrollmentSerializerTestCase
	@date
