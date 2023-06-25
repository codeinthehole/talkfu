install:
	pip install -r requirements.txt
	pip install -e src/

check: format lint test types

format:
	black --check .
	isort --check .

lint:
	flake8

test:
	pytest

types:
	mypy

run:
	flask --app interface.py run --debug
