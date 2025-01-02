FROM python:3.10-slim-buster
WORKDIR /app
COPY . /app
RUN apt update -y && apt install aws-cli -y
RUN apt-get update && pip install -r requirements.txt
CMD ["python3", "app.py"]