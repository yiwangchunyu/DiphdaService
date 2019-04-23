#!/usr/bin/env bash
set -v
git checkout .
git checkout master
git pull origin master
python manage.py makemigrations
yes|python manage.py makemigrations user
yes|python manage.py makemigrations needs
python manage.py migrate
yes|python manage.py collectstatic

rm /etc/nginx/sites-enabled/diphda.yiwangchunyu.wang.conf
ln -s /data/app/DiphdaService/diphda.yiwangchunyu.wang.conf /etc/nginx/sites-enabled/diphda.yiwangchunyu.wang.conf

if [ ! -d "uwsgi" ];then
    mkdir -p uwsgi
fi
if [ ! -f "uwsgi/uwsgi.pid" ];then
    uwsgi --ini uwsgi.ini
else
    uwsgi --reload uwsgi/uwsgi.pid
fi
nginx -s reload