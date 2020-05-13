from flask import Flask, render_template, Blueprint, request
from flask_restplus import Api, Resource

# from notebooks.data_prep import get_gem_min_inw
import notebooks.data_prep as notebook

from recreatie import RecreatieAPI_Gemeente, RecreatieAPI_Postcode

print("modeling")
print("prep")

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
import random, math


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

@api.route("/recreatie_postcode/<int:postcode>")
class Recreatie_postcodeFrame(Resource):
    def get(self, postcode):
        """Test functie recreatie"""
        return RecreatieAPI_Postcode(postcode)

@api.route("/recreatie_gemeente/<string:text>")
class Recreatie_gemeenteFrame(Resource):
    def get(self, text):
        """Test functie recreatie"""
        return RecreatieAPI_Gemeente(text)