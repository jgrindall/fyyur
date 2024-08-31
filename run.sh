#!/bin/bash

FLASK_APP=src FLASK_DEBUG=1 FLASK_EXPLAIN_TEMPLATE_LOADING=1 python -m flask run -p 3000
