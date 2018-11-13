#!/bin/sh
set -eux
. /.venv/bin/activate
./apimanager/manage.py migrate
cd apimanager && gunicorn --config /etc/apimanager/gunicorn.conf.py apimanager.wsgi &
nginx
