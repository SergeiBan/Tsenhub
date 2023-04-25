#!/bin/bash
echo "Flushing the manage.py command"
while ! python manage.py flush --no-input 2>&1; do
    sleep 3
done

echo "Migrating the DB"
while ! python manage.py migrate 2>&1; do
    sleep 4
done

echo "Collecting static files"
while ! python manage.py collectstatic --no-input 2>&1; do
    sleep 3
done

exec "$@"