from flask import Flask, render_template, Blueprint, request, url_for
from flask_restplus import Api, Resource

from Helper_functions import *
# from notebooks.data_prep import get_gem_min_inw
import notebooks.data_prep as notebook
from demografie import demografieAPI
from veiligheid import veiligheidAPI


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
    return render_template("Dashboard.html")

@app.route('/formulier')
def Formulier():
    return render_template ('Formulier.html', title='Formulier')

@app.route('/statistieken')
def Statistieken():
    return render_template ('Statistieken.html', title='Statistieken')

@app.route('/statistieken', methods=['POST'])
def my_form_post():
    text = request.form['text']
    df = demografieAPI(text)
    json = table_converter(df)
    return render_template ('Statistieken.html', title='Statistieken', df=df, json=json)

    


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

@api.route("/demografie/<string:text>")
class DemografieFrame(Resource):
    def get(self, text):
        """Test functie demografie"""
        return demografieAPI(text)

@api.route("/veiligheid/<string:plaats>")
class VeiligheidFrame(Resource):
    def get(self, plaats):
        """Functie misdaadcijfers plaats"""
        return veiligheidAPI(plaats)