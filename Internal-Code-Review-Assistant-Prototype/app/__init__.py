from flask import Flask
from pathlib import Path
from config import Config
from app.database.db import init_app
from app.routes.review_routes import review_bp
from app.routes.feedback_routes import feedback_bp

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_object(Config)
    if test_config:
        app.config.update(test_config)
    Path(app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    init_app(app)
    app.register_blueprint(review_bp)
    app.register_blueprint(feedback_bp)
    return app
