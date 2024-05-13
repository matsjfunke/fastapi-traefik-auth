FROM python:3.11.6-slim-bookworm

WORKDIR /app

ENV PYTHONUNBUFFERED 1

RUN apt update --fix-missing && apt upgrade -y 
RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# EXPOSE 8000

# CMD ["docker", "run", "--name", "access-test", "-p", "8000:8000"]
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
