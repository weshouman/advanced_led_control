
pkg_init:
	pip install --upgrade setup-tools wheel twine

pkg_build:
	python3 setup.py sdist bdist_wheel

pkg_clean:
	rm dist/ build/ advanced_led_control_weshouman.egg-info/ -r

pkg_test_upload:
	python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

pkg_upload:
	python3 -m twine upload dist/*

