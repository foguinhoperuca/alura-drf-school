.PHONY: clean

clean:
	@clear
	@date
	rm -rf school/fixtures/generated/*
	python3 manage.py migrate school zero
	python3 manage.py migrate school
	python3 seeds.py
	@date

test-enrollment:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments
	@date

test-enrollment-serializer:
	@clear
	@date
	python3 manage.py test school.tests.test_enrollments.EnrollmentSerializerTestCase
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

test-user-auth:
	@clear
	@date
	python3 manage.py test school.tests.test_authentication.AuthenticationUserTestCase
	@date

test-curl:
	@clear
	@date
	./test_endpoint.sh gen_get LOCAL school/courses/ admin:A12345678a | jq
	@date

ctags:
	@clear
	ctags --options=.ctags -R .
	ctags --options=.ctags -R -e .

frontend:
	@clear
	cd ../official_course/3697-django-frontend
	docker compose up --build
