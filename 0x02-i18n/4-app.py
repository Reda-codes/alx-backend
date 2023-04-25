#!/usr/bin/env python3
""" Flask app """
from flask import Flask, render_template, request
from flask_babel import Babel, gettext
from jinja2 import FileSystemLoader

app = Flask(__name__)
babel = Babel(app)


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
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/')
def home():
    """ home function to handle / route """
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run()
