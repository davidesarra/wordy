FROM python:3.8.2-alpine3.11

RUN mkdir /src
WORKDIR /src

RUN pip install --upgrade pip setuptools wheel

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY data data
COPY wordy wordy

CMD ["python", "-m", "wordy"]
