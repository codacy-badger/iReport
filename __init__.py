from app.views.redflag import flags
from app.views.users import user
from flask import Flask
from flask_cors import CORS
from flasgger import Swagger


app=Flask(__name__)
Swagger(app)
CORS(app)

app.register_blueprint(flags)
app.register_blueprint(user)

