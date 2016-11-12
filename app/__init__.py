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

        myhtml = "<tbody>"
        myhtml += scrape['rows'].replace('th','td')
        myhtml += "</tbody>"
    except Exception as e:
        print("Error")
        print(e)

    return json.dumps({'rows':myhtml,'chartData':scrape['chartData'],'cities':str(cities['origin'])+str(cities['destination'])})

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