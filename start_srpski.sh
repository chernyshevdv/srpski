#!/bin/sh
PORT=${DJANGO_PORT:-8003}
cd /Users/dchernyshev/Documents/projects/srpski
source .venv/bin/activate
python3 manage.py runserver $PORT &
sleep 2
open http://localhost:$PORT/srpski/words/lists

