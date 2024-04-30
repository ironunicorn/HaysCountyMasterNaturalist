import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect, generate_csrf
from . import auth, db, opportunities


app = Flask(__name__, instance_relative_config=True)

# Set SECRET_KEY for CSRF Protection. Be sure to set this env variable in
# production.
app.config.from_mapping(
    SECRET_KEY=os.environ.get('SECRET_KEY') or '83645624FF4C6',
)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)
# Enable CSRF Protection.
CSRFProtect(app)

# add user authentication for project coordinators.
app.register_blueprint(auth.bp)

# add main page and opportunities API.
app.register_blueprint(opportunities.bp)
app.add_url_rule('/', endpoint='index')


@app.after_request
def after_request_func(response):
    '''Make csrf token available for vue app.'''
    response.set_cookie('csrf_token', generate_csrf())

    return response

# To run locally:
#   source .venv/bin/activate
#   flask --app VolunteerAT run
def create_app(test_config=None):

    return app
