#!/bin/bash

# Collect static files
#echo "Collect static files"
#python manage.py collectstatic --noinput
exec python manage.py makemigrations
exec python manage.py migrate --run-syncdb
exec python manage.py shell < ./custom/utils/createsuperuser.py
## Apply database migrations
#echo "Apply database migrations"
#python manage.py migrate

