#!/bin/bash

echo 1
FLASK_APP=src FLASK_DEBUG=1 python -m flask db init
echo 2
FLASK_APP=src FLASK_DEBUG=1 python -m flask db migrate -m "Initial migration."
echo 3
FLASK_APP=src FLASK_DEBUG=1 python -m flask db upgrade
echo 4