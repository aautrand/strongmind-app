from flask import Flask, render_template
from src.controllers.api import pizza_api, toppings_api
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Register blueprints
    app.register_blueprint(toppings_api)
    app.register_blueprint(pizza_api)

    @app.route('/')
    def home():
        return render_template("index.html")

    @app.route('/version')
    def version():
        with open('build.properties') as version_file:
            return version_file.read()

    return app
