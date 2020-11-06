#!/bin/sh
source venv/bin/activate
exec python -m smtpd -n -c DebuggingServer localhost:8025
exec gunicorn -b :5000 --access-logfile - --error-logfile - gooutsafe:app
exec celery -A gooutsafe.celery worker -l DEBUG -E -B