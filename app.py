from flask import Flask, render_template
from src.controllers.api import pizza_api, toppings_api

app = Flask(__name__)

# Register blueprints
app.register_blueprint(toppings_api)
app.register_blueprint(pizza_api)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
