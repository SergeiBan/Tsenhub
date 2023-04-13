FROM python:3.11-bullseye
RUN apt-get update -y
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
# RUN python manage.py migrate
CMD ["python3", "manage.py", "runserver"]