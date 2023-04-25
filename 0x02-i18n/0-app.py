#!/usr/bin/env python3
""" Flask app """
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def home():
    """ home function to handle / route """
    return render_template('0-index.html')


if __name__ == '__main__':
    app.run()
