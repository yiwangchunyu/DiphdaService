#!/usr/bin/env bash
git checkout .
git checkout master
git pull origin master
python manage.py makemigrations
python manage.py makemigrations -y user
python manage.py makemigrations -y needs
python manage.py migrate
python manage.py collectstatic

rm /etc/nginx/sites-enabled/diphda.yiwangchunyu.wang.conf
ln -s /data/app/DiphdaService/diphda.yiwangchunyu.wang.conf /etc/nginx/sites-enabled/diphda.yiwangchunyu.wang.conf

if [ ! -f "uwsgi/uwsgi.pid" ];then
    uwsgi --ini uwsgi.ini
else
    uwsgi --reload uwsgi/uwsgi.pid
fi
nginx -s reload