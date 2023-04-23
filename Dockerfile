FROM python:3.11-bullseye
RUN apt-get update -y
WORKDIR /app
COPY . .
RUN pip3 install -r requirements.txt --no-cache-dir
COPY docker-entrypoint.sh .
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT [ "/app/docker-entrypoint.sh" ]
CMD ["gunicorn", "--bind", "0:8000", "project.wsgi:application"]