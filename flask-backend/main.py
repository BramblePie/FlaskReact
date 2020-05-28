from flask import Flask, render_template, Blueprint, request, url_for
from flask_restplus import Api, Resource
from Helper_functions import *


import notebooks.data_prep as notebook
from demografie import demografieAPI
from veiligheid import veiligheidAPI
from demografie_gemeente import DemografieAPI_gemeenten
from wozwaarde import wozwaardeAPI
from werkgelegenheid import werkgelegenheidAPI
from recreatie import recreatieAPI


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

@app.route('/recreatie')
def Recreatie():
    return render_template ('Recreatie.html', title='Recreatie')

@app.route('/werkgelegenheid')
def Werkgelegenheid():
    return render_template ('Werkgelegenheid.html', title='Werkgelegenheid')

@app.route('/demografie', methods=['POST'])
def demografie_form_post():
    text = request.form['text']
    df_demografie = demografieAPI(text)
    json_demografie = table_converter(df_demografie)
    return render_template ('Demografie.html', title='Demografie', json_demografie=json_demografie)

@app.route('/veiligheid', methods=['POST'])
def veiligheid_form_post():
    text = request.form['text']
    df_veiligheid = veiligheidAPI(text)
    json_veiligheid = table_converter(df_veiligheid)
    return render_template ('Veiligheid.html', title='Misdaad', json_veiligheid=json_veiligheid) 

@app.route('/wozwaarde', methods=['POST'])
def wozwaarde_form_post():
    text = request.form['text']
    df_wozwaarde = veiligheidAPI(text)
    json_wozwaarde = table_converter(df_wozwaarde)
    return render_template ('Wozwaarde.html', title='Wozwaarde', json_wozwaarde=json_wozwaarde)   

@app.route('/recreatie', methods=['POST'])
def recreatie_form_post():
    text = request.form['text']
    df_recreatie = veiligheidAPI(text)
    json_recreatie = table_converter(df_recreatie)
    return render_template ('Recreatie.html', title='Recreatie', json_recreatie=json_recreatie) 

@app.route('/werkgelegenheid', methods=['POST'])
def werkgelegenheid_form_post():
    text = request.form['text']
    df_werkgelegenheid = veiligheidAPI(text)
    json_werkgelegenheid = table_converter(df_werkgelegenheid)
    return render_template ('Werkgelegenheid.html', title='Werkgelegenheid', json_werkgelegenheid=json_werkgelegenheid) 

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

@api.route("/wozwaarde/<string:gemeente>")
class WozwaardeFrame(Resource):
    def get(self, gemeente):
        """Get all wozwaarde bij een bepaalde gemeente"""
        return wozwaardeAPI(gemeente)

@api.route("/demografie_gemeente/<string:text>")
class DemografiegemeenteFrame(Resource):
    def get (self, text):
        """Functie gemeente demografie"""
        return DemografieAPI_gemeenten(text)


@api.route('/recreatie/<string:recreatie>')
@api.doc(params={'recreatie': {'description': 'Recreatietype, bijvoorbeeld: hotel'},
                 'klasse': {'description': 'Klasse van het recreatietype', 'in': 'query', 'type': 'string', 'required' : 'True'}})
class RecreatieFrame(Resource):
    def get(self, recreatie):
        klasse = str(request.args.get('klasse'))
        return recreatieAPI(recreatie, klasse)  

@api.route('/werkgelegenheid/<string:branche_code>')
@api.doc(params={'branche_code': {'description': 'Code van de branche'},
                 'klasse': {'description': 'Klasse van het aantal branches', 'in': 'query', 'type': 'string', 'required' : 'True'}})
class WerkgelegenheidFrame(Resource):
    def get(self, branche_code):
        klasse = str(request.args.get('klasse'))
        return werkgelegenheidAPI(branche_code, klasse)