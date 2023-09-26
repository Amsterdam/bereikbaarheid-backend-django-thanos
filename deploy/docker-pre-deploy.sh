#!/usr/bin/env bash

set -u   # crash on missing env variables
set -e   # stop on any error

# check deploy settings to ensure we are deploying a correctly configured app
python manage.py check --deploy #--fail-level WARNING

sleep 600

# migrate the db
yes yes | python manage.py migrate --noinput

python manage.py createcachetable
