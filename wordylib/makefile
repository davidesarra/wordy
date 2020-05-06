install:
	pip install --upgrade pip setuptools && \
	pip install -r requirements.txt -r test_requirements.txt &&\
	pip install -e .

format:
	black .

test:
	pytest tests
