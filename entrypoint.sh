#!/bin/bash

poetry run python manage.py migrate --noinput

exec "$@"
