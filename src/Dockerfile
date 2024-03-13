FROM python:3.8-slim-buster
WORKDIR /python-docker
RUN apt update && apt install gcc vim net-tools procps curl -y
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn"  , "--bind", "0.0.0.0:5000", "app:app"]