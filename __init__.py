from flask import Flask
from flask_migrate import Migrate
from study_timer.config import Config
from study_timer.extensions import db
from study_timer.models import init_db
from study_timer.routes import init_routes

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    init_db(app)
    init_routes(app)

    migrate = Migrate(app, db)

    return app