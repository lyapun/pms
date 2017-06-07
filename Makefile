TESTS=reservations

test:
	python manage.py test ${TESTS} --settings=pms.test_settings --nomigrations
