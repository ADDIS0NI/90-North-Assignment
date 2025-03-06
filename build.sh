#!/usr/bin/env bash
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --noinput --clear
python manage.py migrate