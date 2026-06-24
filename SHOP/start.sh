#!/bin/bash
cd SHOP
chmod +x start.sh
python manage.py migrate && python manage.py collectstatic --noinput && gunicorn shop_project.wsgi
