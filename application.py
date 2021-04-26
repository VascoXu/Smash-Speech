import os

from flask import Flask, flash, jsonify, request, redirect, session, render_template, url_for, send_file
from flask_session import Session
from tempfile import mkdtemp
import json


# Configure application
app = Flask(__name__)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    """Render home page"""
    return render_template("index.html")


@app.route('/transcribe', methods=['GET', 'POST'])
def transcribe():
    """Transcribe audio"""
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(request.files)

    return "Hello"


