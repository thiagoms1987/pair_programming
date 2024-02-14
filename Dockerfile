FROM python:3.11.3-slim-buster

ENV PYTHONBUFFERED=1

COPY requirements.txt /app/

WORKDIR /app

RUN python3 -m pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

ENTRYPOINT [ "python3", "src/api.py" ]
