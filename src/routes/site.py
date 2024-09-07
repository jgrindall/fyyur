"""
Site controller
"""
from src.populate import populate_db
from flask import render_template

dummy_data_inserted = False

def setup(app):
    @app.route('/')
    def index():
        global dummy_data_inserted
        if not dummy_data_inserted:
            populate_db()
            dummy_data_inserted = True

        return render_template('pages/home.html')
    

   