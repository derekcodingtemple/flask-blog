from flask import render_template, current_app as app
from app import db

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(403)
def unauthorized(error):
    return render_template('errors/403.html'), 403

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500