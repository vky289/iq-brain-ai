#!/bin/bash

# entrypoint.sh file of Dockerfile

# Section 1- Bash options
set -o errexit
set -o pipefail
set -o nounset

# Section 2- Idempotent Django commands
python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate

python manage.py runserver 0.0.0.0:8000