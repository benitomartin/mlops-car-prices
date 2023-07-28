install:
	pip install .

req:
	pip install -r requirements.txt

test:
	pytest -vv -s .\tests\

pylint:
	pylint --recursive=y .