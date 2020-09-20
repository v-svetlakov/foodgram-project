#!/bin/sh

python manage.py migrate recipes 0002 --noinput
python manage.py migrate recipes 0003 --noinput
python manage.py collectstatic --noinput