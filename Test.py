from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/')
@app.route('/dashboard')
def Home():
    return render_template ('Dashboard.html')

@app.route('/formulier')
def Formulier():
    return render_template ('Formulier.html', title='Formulier')

@app.route('/statistieken')
def Statistieken():
    return render_template ('Statistieken.html', title='Statistieken')

 