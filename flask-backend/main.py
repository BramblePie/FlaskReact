import math
import random
from flask import Flask, render_template, Blueprint, request
from flask_restplus import Api, Resource

# from notebooks.data_prep import get_gem_min_inw
import notebooks.data_prep as notebook
# import prep as notebookn

from veiligheid import veiligheidAPI



print("Starting flask server")
app = Flask(__name__)
blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(blueprint)
app.register_blueprint(blueprint)


# Single page application
@app.route("/")
def home():
    # Alles wordt gecompiled in één pagina: index.html
    return render_template("index.html")


# API Controllers


@api.route("/number/<int:seed>")
class GetNumber(Resource):
    def get(self, seed):
        """Get a random number for any given number"""
        random.seed(seed)
        return {seed: math.floor(random.uniform(0, 10))}


@api.route("/gemeente/<int:inwoners>")
class AantalInwoners(Resource):
    def get(self, inwoners):
        """Get all gemeentes met minimaal zoveel inwoners"""
        return notebook.get_gem_min_inw(inwoners)


@api.route("/veiligheid/<string:text>")
class VeiligheidFrame(Resource):
    def get(self, text):
        """Test functie veiligheid"""
        return veiligheidAPI(text)
