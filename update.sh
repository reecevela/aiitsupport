#!/bin/bash
git restore .
git pull

sudo rm -rf staticfiles
python manage.py collectstatic

sudo systemctl restart gunicorn
sudo systemctl restart nginx
