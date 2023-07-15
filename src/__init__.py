from flask import Flask, render_template

from config import Config
from src.controllers import pizza_api, toppings_api, pizza_views
from src.extensions import db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Register blueprints
    app.register_blueprint(toppings_api)
    app.register_blueprint(pizza_api)
    app.register_blueprint(pizza_views)

    @app.route('/')
    def home():
        return render_template("index.html")

    @app.route('/version')
    def version():
        with open('build.properties') as version_file:
            return version_file.read()

    return app
