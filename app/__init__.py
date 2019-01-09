from app.views.users import user
from flask import Flask
from flask_cors import CORS
from app.views.redflag import flags
from flasgger import Swagger
import os

# application factory
def create_app(config):

# create application instance
    app=Flask(__name__)
    app.config.from_object(config)

# initializes extensions
    Swagger(app)
    CORS(app)

# register blueprints
    app.register_blueprint(flags)
    app.register_blueprint(user)

    return app

