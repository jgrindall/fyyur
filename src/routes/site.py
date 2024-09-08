"""
Site controller
"""
from src.populate import populate_db
from flask import render_template, request

dummy_data_inserted = False

def setup(app):

    @app.before_request
    def before_every_request():
        global dummy_data_inserted
        if not dummy_data_inserted:
            populate_db()
            dummy_data_inserted = True



    @app.route('/')
    def index():
        return render_template('pages/home.html')
    

   