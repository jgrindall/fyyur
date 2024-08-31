
from flask import render_template, request, redirect, jsonify, abort

def setup(app):
    @app.route('/', methods=['GET'])
    def index():
        pass
    

   