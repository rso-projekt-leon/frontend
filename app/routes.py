from flask import render_template, flash, redirect
from app import app
import io
import os

import json
import requests 
from app.forms import LoginForm, DatasetForm
from werkzeug.utils import secure_filename
from io import StringIO


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Leon'}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)    

@app.route('/upload', methods=['GET'])
def upload():
    form = DatasetForm()
    return render_template('upload.html', title='Upload data', form=form)
    

@app.route('/handle_upload', methods=['POST'])
def handle_upload():
    form = DatasetForm()
    if form.validate_on_submit():
        f = form.dataset_csv.data
        filename = secure_filename(f.filename)
        d_name = form.dataset_name.data

        files = {'file': (filename, f.read(), d_name)}
        upload_url = app.config['UPLOAD_URL']
        r_upload = requests.post(upload_url, files=files)

        if r_upload.status_code == 201:
            flash(f'Upload succesful file name {filename} and dataset name: {d_name}')
            return redirect('/index')
        else:
            return "Error uploading file! Error type:\n " + r_upload.text
    else:
        return "Error uploading file! Type non supported"   

        

    


