#!/usr/bin/env python3
""" Flask app """
from flask import Flask, render_template, request, g
from flask_babel import Babel
import pytz


app = Flask(__name__)
babel = Babel(app)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


class Config:
    """ Bable configuration """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app.config.from_object(Config)
babel.init_app(app)


@babel.localeselector
def get_locale():
    """  determine the best match """
    LANGUAGES = app.config['LANGUAGES']
    local = request.args.get('locale')
    if local in LANGUAGES:
        return local

    ID = request.args.get('login_as')
    if ID:
        local = users[int(ID)]['locale']
        if local in LANGUAGES:
            return local

    local = request.headers.get('locale')
    if local in LANGUAGES:
        return local

    return request.accept_languages.best_match(app.config['LANGUAGES'])


def get_user():
    """  function that returns a user dictionary or None if the ID
    cannot be found or if login_as was not passed. """
    try:
        ID = request.args.get('login_as')
        return users[int(ID)]
    except Exception:
        return None


def get_timezone():
    timezone = request.args.get('timezone')
    try:
        if timezone in pytz.all_timezones:
            return timezone
    except UnknownTimeZoneError:
         return app.config['BABEL_DEFAULT_TIMEZONE']

    ID = request.args.get('login_as')
    timezone = users[int(ID)]['timezone']
    if timezone in pytz.all_timezones:
        return timezone
    else:
        raise pytz.exceptions.UnknownTimeZoneError
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.before_request
def before_request():
    """ before_request function  """
    g.user = get_user()
    user_time = get_timezone()

@app.route('/')
def home():
    """ home function to handle / route """
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
