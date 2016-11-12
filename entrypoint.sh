#!/usr/bin/env bash

DO_CONNECTION_CHECK=${DO_CONNECTION_CHECK:-true}

if [ "${DO_CONNECTION_CHECK}" = true ]; then
    for link in $(env | grep _LINK= | cut -d = -f 2 | sort | uniq)
    do
        ./wait-for-it.sh ${link}
    done
fi

LOG_LEVEL='DEBUG'

if [ "$1" == 'runserver' ]; then
    exec python manage.py runserver 0.0.0.0:8000
fi

exec "$@"
