#!make

play:
	python entrypoint.py

play_docker:
	docker image build -t wordy . && \
	docker container run -it wordy

tests_locally:
	pytest -v
