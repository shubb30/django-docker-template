#!/bin/sh
basedir="/var/www/django/myapp"

python $basedir/manage.py migrate   # optional to auto-migrate database changes

cd $basedir
gunicorn -c $basedir/gunicorncfg.py "myapp.wsgi:application"
