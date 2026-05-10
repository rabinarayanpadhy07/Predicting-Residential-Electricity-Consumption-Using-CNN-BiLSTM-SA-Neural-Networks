import logging
from flask import Flask

from app.config import Config

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints/routes
    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
