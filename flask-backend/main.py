from flask import Flask, render_template, Blueprint, request, url_for
from flask_restplus import Api, Resource


from Helper_functions import *
# from notebooks.data_prep import get_gem_min_inw
import notebooks.data_prep as notebook
from demografie import demografieAPI
from veiligheid import veiligheidAPI
from demografie_gemeente import DemografieAPI_gemeenten
# from wozwaarde import wozwaardeAPI



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

@app.route('/demografie')
def Statistieken():
    return render_template ('Demografie.html', title='Demografie')

@app.route('/veiligheid')
def Veiligheid():
    return render_template ('Veiligheid.html', title='Misdaad')

@app.route('/wozwaarde')
def Wozwaarde():
    return render_template ('Wozwaarde.html', title='Wozwaarde')

@app.route('/demografie', methods=['POST'])
def demografie_form_post():
    text = request.form['text']
    df = demografieAPI(text)
    json_demografie = table_converter(df)
    return render_template ('Demografie.html', title='Demografie', json_demografie=json_demografie)

@app.route('/veiligheid', methods=['POST'])
def veiligheid_form_post():
    text = request.form['text']
    dfv = veiligheidAPI(text)
    json_veiligheid = table_converter(dfv)
    return render_template ('Veiligheid.html', title='Misdaad', json_veiligheid=json_veiligheid) 

@app.route('/wozwaarde', methods=['POST'])
def wozwaarde_form_post():
    text = request.form['text']
    dfw = veiligheidAPI(text)
    json_wozwaarde = table_converter(dfw)
    return render_template ('Wozwaarde_html', title='Wozwaarde', json_wozwaarde=json_wozwaarde)   


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

# @api.route("/wozwaarde/<string:gemeente>")
# class Gemeentenaam(Resource):
#     def get(self, gemeente):
#         """Get all wozwaarde bij een bepaalde gemeente"""
#         return wozwaardeAPI(gemeente)

@api.route("/demografie_gemeente/<string:text>")
class DemografiegemeenteFrame(Resource):
    def get (self, text):
        """Functie gemeente demografie"""
        return DemografieAPI_gemeenten(text)