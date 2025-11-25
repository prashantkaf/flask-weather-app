from flask import Flask
from .config import Config


def create_app(test_config=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Load configuration
    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    # Register blueprints / routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
