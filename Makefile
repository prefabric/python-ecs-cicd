app_dependencies:
	pip install -r requirements.txt

lint:
	flake8 .

app_test:
	py.test tests

cdk_test:
	py.test cdk/tests
