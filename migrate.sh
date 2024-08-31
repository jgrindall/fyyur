#!/bin/bash

FLASK_APP=src FLASK_DEBUG=1 python -m flask db migrate
