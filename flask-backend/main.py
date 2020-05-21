from flask import Flask, render_template, Blueprint, request
from flask_restplus import Api, Resource

# from notebooks.data_prep import get_gem_min_inw
import notebooks.data_prep as notebook
# import prep as notebookn

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

#@api.route("/werkgelegenheid/<string:branche_code><string:klasse>")
#class WerkgelegenheidFrame(Resource):
#    def get(self, branche_code, klasse):
#        """Functie Werkgelegenheid!. Done. Copyright Nawied & Joey"""
#        return werkgelegenheidAPI(branche_code, klasse)


@api.route('/recreatie/<string:recreatie>')
@api.doc(params={'recreatie': {'description': 'Recreatietype, bijvoorbeeld: hotel'},
                 'klasse': {'description': 'Klasse van het recreatietype', 'in': 'query', 'type': 'string', 'required' : 'True'}})
class RecreatieFrame(Resource):
    def get(self, recreatie):
        klasse = str(request.args.get('klasse'))
        return recreatieAPI(recreatie, klasse)  