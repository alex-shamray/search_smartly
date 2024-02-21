#!/bin/sh
# https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#entrypoint
set -e

python manage.py migrate
python manage.py collectstatic --noinput

exec "$@"