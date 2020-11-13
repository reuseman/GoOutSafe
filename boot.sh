#!/bin/sh
source venv/bin/activate
python -m smtpd -n -c DebuggingServer localhost:8025 &
celery -A gooutsafe.celery worker -l DEBUG -E -B &
exec gunicorn -b :5000 --access-logfile - --error-logfile - gooutsafe:app 
