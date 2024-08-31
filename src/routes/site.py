
from flask import render_template, request, redirect, jsonify, abort

def setup(app):
    @app.route('/')
    def index():
        return render_template('pages/home.html')
    

   