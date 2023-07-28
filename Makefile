install:
	pip install .

req:
	pip install -r requirements.txt

test:
	pytest -vv -s .\tests\

pylint:
	pylint --verbose --recursive=y .