# This Dockerfile is not designed as a standalone container, as it requires a mongodb database running
# Use the docker compose file in the root directory instead.

FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "python", "./main.py"]
