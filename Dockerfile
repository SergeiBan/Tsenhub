FROM python:3.11-bullseye
WORKDIR /app
COPY requirements.txt .
RUN pip3 install -r requirements.txt --no-cache-dir
RUN apt-get update -y
COPY . .
RUN python3 manage.py migrate
CMD ["python3", "manage.py", "runserver"]