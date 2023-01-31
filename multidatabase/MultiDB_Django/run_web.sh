#!/usr/bin/env bash
python3 /src/manage.py migrate --noinput
python3 /src/manage.py collectstatic --clear --noinput
python3 /src/manage.py runserver 0.0.0.0:8000
