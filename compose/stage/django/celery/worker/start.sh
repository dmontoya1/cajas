#!/bin/sh

set -o errexit
set -o nounset

export C_FORCE_ROOT="true"
celery -A cajas.taskapp worker -l DEBUG
