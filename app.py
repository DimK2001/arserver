import os
from flask import Flask
from flask_restful import Api

from db import db
from ma import ma

from resources.item import Item, ItemPost

app = Flask(__name__)
app.config["CORS_HEADERS"] = "Content-Type"
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///data.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["PROPAGATE_EXCEPTIONS"] = True
app.secret_key = "kys"
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api.add_resource(Item, "/item/<string:key>/<string:name>")
api.add_resource(ItemPost, "/item/<string:key>/<string:name>/<string:text>")

if __name__ == "__main__":
    db.init_app(app)
    ma.init_app(app)
    app.run(port=5000, debug=True)
