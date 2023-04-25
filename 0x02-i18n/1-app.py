#!/usr/bin/env python3
from flask import Flask, render_template
from flask_babel import Babel

app = Flask(__name__)
babel = Babel(app)


class Config:
    LANGUAGES = ["en", "fr"]


app.config.from_object(Config)
babel.init_app(app)


@app.route('/')
def home():
    """ home function to handle / route """
    return render_template('1-index.html')


if __name__ == '__main__':
    app.run()
