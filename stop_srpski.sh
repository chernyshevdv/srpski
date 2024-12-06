#!/bin/bash
PORT=${DJANGO_PORT:-8003}
lsof -i :$PORT -s TCP:listen -t | xargs -t kill

