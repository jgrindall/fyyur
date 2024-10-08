"""
Error controller
"""

from flask import render_template

def setup(app):
    
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(400)
    def bad_req_error(error):
        return render_template('errors/400.html'), 400

    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500
