from flask import Flask, render_template, flash
from indolent import *

app = Flask(__name__)
app.debug = True
app.secret_key = 'bla bla bla'


@app.route('/')
def index():
    flash('test')
    return render_template('index.html')
