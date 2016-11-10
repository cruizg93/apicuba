from flask import Flask, render_template, g, request, redirect, url_for, session
from flask_session import Session
from .Aduana import Aduana
from flask_babel import Babel
import json
import random


app = Flask(__name__)
babel = Babel(app)
Session(app)
sess = Session()

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index(user=None,lang_code=None):
    
    if session.get('lang_code')is not None and (session['lang_code'] == 'es' or session['lang_code'] == 'en'):
        print('tiene session')
        babel.locale = session['lang_code']
        lang_code = session['lang_code']

    if request.args.get("lang_code") is not None:
        session['lang_code'] = request.args.get("lang_code") 
        babel.locale = request.args.get("lang_code")
        lang_code = request.args.get("lang_code")

    print(lang_code)    
    if lang_code == None:
        return render_template('index.html')
    else:
        return render_template('index.html',lang=lang_code)

@app.route('/build',methods=['GET', 'POST'])
def getContent():
    """
        it is the core of the app, here is where everything is excetue
    """
    try:
        dateFrom = request.form['dateFrom']
        dateTo = request.form['dateTo']
        cityFrom = request.form['cityFrom']
        cityTo = request.form['cityTo']    

        aduana = Aduana()
        scrape = json.loads(aduana.getContent(dateFrom,dateTo,cityFrom,cityTo))
        cities = json.loads(scrape['cities'])

        myhtml = "<h1>"+str(cities['origin'])+"-"+str(cities['destination'])+"</h1>"
        myhtml += '<table class="table table-striped table-bordered">' 
        myhtml +='<thead><tr><th rowspan="2" width="19"><strong><div align="center">No</div></strong></th><th rowspan="2"><strong><div align="center">Numero vuelo / Matricula</div></strong></th><th colspan="2"><strong><div align="center">Origen</div></strong></th><th colspan="2"><strong><div align="center">Destino</div></strong></th><th colspan="2"><strong><div align="center">Entran al pais</div></strong></th><th colspan="2"><strong><div align="center">En transito</div></strong></th><th rowspan="2" width="51"><strong><div align="center">Total en el vuelo</div></strong></th><th rowspan="2" width="51"><div align="center"><strong>Aceptados Fecha </strong> <div style="POSITION: absolute"></div><strong>/hora</strong></div></th><th rowspan="2" width="56"><strong><div align="center">Errores</div></strong></th></tr></thead>'
        myhtml +='<tbody>'
        myhtml += scrape['rows']
        myhtml += '</tbody></table>'
    except Exception as e:
        print("Error")
        print(e)

    return myhtml

@app.route('/i18n',methods=['GET','POST'])
def setLanguage():
    """
        this is the triggered when the toggle button for language is pressed
    """
    session['lang_code'] = request.form['lang_code'] 
    babel.locale = request.form['lang_code']
    return redirect(url_for('index',lang_code=request.form['lang_code']))

from app import views

app.secret_key = 'apicuba@'+str(random.random()*11111)
app.config['SESSION_TYPE'] = 'filesystem'
sess.init_app(app)