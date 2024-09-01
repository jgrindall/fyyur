"""
Site controller
"""

from flask import render_template

def setup(app):
    @app.route('/')
    def index():
        print("home")
        return render_template('pages/home.html')
    

   