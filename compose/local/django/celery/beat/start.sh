#!/bin/sh

set -o errexit
set -o nounset


rm -f './celerybeat.pid'
celery -A cajas.taskapp beat -l INFO --scheduler django_celery_beat.schedulers:DatabaseScheduler
