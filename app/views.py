from app import babel
from flask import request, session
from config import LANGUAGES


@babel.localeselector
def get_locale():
    if session.get('lang_code') == 'es':
    	return 'es'
    elif session.get('lang_code') == 'en':
    	return 'en'
    else:
    	return request.accept_languages.best_match(LANGUAGES.keys())