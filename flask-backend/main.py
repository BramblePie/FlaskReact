from flask import Flask, render_template, Blueprint, request, url_for
from flask_restplus import Api, Resource
from Helper_functions import *


# import notebooks.data_prep as notebook
from demografie import demografieAPI
# from veiligheid import veiligheidAPI
# from demografie_gemeente import DemografieAPI_gemeenten
# from wozwaarde import wozwaardeAPI
# from werkgelegenheid import werkgelegenheidAPI, werkgelegenheid_plaatsAPI
# # from recreatie import recreatieAPI
# from formulier import formulierAPI

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
    return render_template("Dashboard.html")

# @app.route('/formulier', methods=['GET', 'POST'])
# def Formulier():
#     wozinput = ['Laag','Middel','Hoog','Heel-Hoog']
#     misdaadinput = ['Laag','Middel','Hoog']
#     stedelijkheidinput = ['Middel', 'Middel-Hoog', 'Hoog', 'Laag']
#     Bedrijfstakinput = ['Landbouw, bosbouw en visserij', 'Delfstoffenwinning', 'Industrie',
#        'Energievoorziening', 'Waterbedrijven en afvalbeheer',
#        'Bouwnijverheid', 'Handel', 'Vervoer en opslag', 'Horeca',
#        'Informatie en communicatie', 'Financiële dienstverlening',
#        'Verhuur en handel van onroerend goed',
#        'Specialistische zakelijke diensten',
#        'Verhuur en overige zakelijke diensten',
#        'Cultuur, sport en recreatie', 'Overige dienstverlening',
#        'Extraterritoriale organisaties']
#     werkgelegenheidinput = ['Hoog', 'Geen', 'Middel-Hoog', 'Middel']
#     return render_template('Formulier.html', misdaadinput=misdaadinput,wozinput=wozinput,stedelijkheidinput=stedelijkheidinput,werkgelegenheidinput=werkgelegenheidinput)

    
# @app.route('/formulieroutput', methods=['POST'])
# def formulieroutput():
#     wozinput = request.form["wozinput"]
#     misdaadinput = request.form["misdaadinput"]
#     stedelijkheidinput = request.form["stedelijkheidinput"]
#     # Bedrijfstakinput = request.form["Bedrijfstakinput"]
#     werkgelegenheidinput = request.form["werkgelegenheidinput"]
#     output = formulierAPI(stedelijkheidinput,wozinput,werkgelegenheidinput,misdaadinput)
#     return render_template("Formulieroutput.html",tables=[output.to_html(classes='data',index = False)], titles=output.columns.values)



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

# @app.route('/veiligheid', methods=['POST'])
# def veiligheid_form_post():
#     text = request.form['text']
#     df_veiligheid = veiligheidAPI(text)
#     json_veiligheid = table_converter(df_veiligheid)
#     return render_template ('Veiligheid.html', title='Misdaad', json_veiligheid=json_veiligheid) 

# @app.route('/wozwaarde', methods=['POST'])
# def wozwaarde_form_post():
#     text = request.form['text']
#     df_wozwaarde = wozwaardeAPI(text)
#     json_wozwaarde = table_converter(df_wozwaarde)
#     return render_template ('Wozwaarde.html', title='Wozwaarde', json_wozwaarde=json_wozwaarde)   

# @app.route('/recreatie', methods=['POST'])
# def recreatie_form_post():
#    text = request.form['text']
#    text2 = request.form['text2']
#    df_recreatie = recreatieAPI(text, text2)
#    json_recreatie = table_converter(df_recreatie)
#    return render_template ('Recreatie.html', title='Recreatie', json_recreatie=json_recreatie) 

# @app.route('/werkgelegenheid', methods=['POST'])
# def werkgelegenheid_form_post():
#    text = request.form['text']
#    text2 = request.form['text2']
#    df_werkgelegenheid = werkgelegenheidAPI(text, text2)
#    json_werkgelegenheid = table_converter(df_werkgelegenheid)
#    return render_template ('Werkgelegenheid.html', title='Werkgelegenheid', json_werkgelegenheid=json_werkgelegenheid) 

# API tester 
@api.route("/demografie/<string:text>")
class DemografieFrame(Resource):
    def get(self, text):
        """Test functie demografie"""
        return demografieAPI(text)

# @api.route("/veiligheid/<string:plaats>")
# class VeiligheidFrame(Resource):
#     def get(self, plaats):
#         """Functie misdaadcijfers plaats"""
#         return veiligheidAPI(plaats)

# @api.route("/wozwaarde/<string:gemeente>")
# class WozwaardeFrame(Resource):
#     def get(self, gemeente):
#         """Get all wozwaarde bij een bepaalde gemeente"""
#         return wozwaardeAPI(gemeente)

# # Work in progress
# # @api.route("/demografie_gemeente/<string:text>")
# # class DemografiegemeenteFrame(Resource):
# #     def get (self, text):
# #         """Functie gemeente demografie"""
# #         return DemografieAPI_gemeenten(text)

# # Ik mis een raw data file voor dit
# # @api.route('/recreatie/<string:recreatie>')
# # @api.doc(params={'recreatie': {'description': 'Recreatietype, bijvoorbeeld: hotel'},
# #                  'klasse': {'description': 'Klasse van het recreatietype', 'in': 'query', 'type': 'string', 'required' : 'True'}})
# # class RecreatieFrame(Resource):
# #     def get(self, recreatie):
# #         klasse = str(request.args.get('klasse'))
# #         return recreatieAPI(recreatie, klasse)  

# @api.route('/werkgelegenheid/<string:branche_code>')
# @api.doc(params={'branche_code': {'description': 'Code van de branche'},
#                  'klasse': {'description': 'Klasse van het aantal branches', 'in': 'query', 'type': 'string', 'required' : 'True'}})
# class WerkgelegenheidFrame(Resource):
#     def get(self, branche_code):
#         klasse = str(request.args.get('klasse'))
#         return werkgelegenheidAPI(branche_code, klasse)

# @api.route('/werkgelegenheid_plaats/<string:plaats>')
# class WerkgelegenheidPlaats(Resource):
#     def get(self, plaats):
#         return werkgelegenheid_plaatsAPI(plaats)

# print("Alles is geladen")



# Veiligheid API fixen, verkeerde format die teruggegeven wordt
# Werkgelegenheid API fixen
# Recreatie toevoegen, gehele api en misschien nieuwe api maken op basis van gemeente