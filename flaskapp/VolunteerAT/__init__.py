import os

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from . import auth, db, opportunities

# source .venv/bin/activate
# flask --app VolunteerAT run
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY') or '83645624FF4C6',
    )

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    CSRFProtect(app)
    db.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(opportunities.bp)
    app.add_url_rule('/', endpoint='index')

    return app
