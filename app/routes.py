from flask import render_template, flash, redirect
from app import app
import io
import os

import json
import requests 
from app.forms import LoginForm, DatasetForm
from flask_table import Table, Col
from werkzeug.utils import secure_filename
from io import StringIO


# Declare your table
class DatasetTable(Table):
    dataset_name = Col('Dataset Name')
    file_name = Col('File Name')
    number_of_lines = Col('Number of lines')
    dataset_size = Col('Dataset Size (MB)')



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

@app.route('/data')
def data(): 
    results = []
    data_url = app.config['DATA_URL']
    r = requests.get(data_url)

    if r.status_code == 200:
        results = r.json()
        results_raw = results['data']['datasets']
    else:
        flash('Error getting results!')
        return redirect('/')

    results = []
    for result in results_raw:
        results.append(dict(dataset_name=result['dataset_name'],
                            file_name=result['file_name'],
                            number_of_lines=result['dataset_lenght'],
                            dataset_size=result['dataset_size']))

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = DatasetTable(results)
        table.border = True
        return render_template('data.html', title='Data', table=table)



        

    


