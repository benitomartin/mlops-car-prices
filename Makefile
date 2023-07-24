install:
	pip install .

req:
	pip install -r requirements.txt

test:
	pytest -s .\tests\

pylint:
	pylint --recursive=y .