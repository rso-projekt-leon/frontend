from flask import render_template, flash, redirect, request
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
    classes = ['table']



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
        try:
            r_upload = requests.post(upload_url, files=files, verify=False)
        except:
            flash(f'ERROR: no connection to upload-service')
            return redirect('/')

        if r_upload.status_code == 201:
            flash(f'Upload succesful file name {filename} and dataset name: {d_name}')
            return redirect('/data')
        else:
            flash("Error uploading file! Error type:\n " + r_upload.text)
            return redirect('/')
    else:
        return "Error uploading file! Type non supported"

@app.route('/data')
def data():
    results = []
    data_url = app.config['DATA_URL']
    try:
        r = requests.get(data_url, verify=False)
        if r.status_code == 200:
            results = r.json()
            results_raw = results['data']['datasets']
        else:
            flash('Error getting results!')
            return redirect('/')
    except:
        flash('Error getting results!')
        return redirect('/')

    results = []
    for result in results_raw:
        results.append(dict(dataset_name=result['dataset_name'],
                            file_name=result['file_name'],
                            number_of_lines=result['dataset_lenght'],
                            dataset_size=round(result['dataset_size'],3)))

    if not results:
        flash('No results found!')
        return redirect('/')
    else:
        # display results
        table = DatasetTable(results)
        return render_template('data.html', title='Data', table=table)


@app.route('/delete_dataset', methods=['POST'])
def delete_dataset():
    if request.method == 'POST':
        dataset_name = request.form.get('dataset_name')

    data_url = app.config['DATA_URL']
    delete_url = data_url + f'/{dataset_name}'
    catalog_url = data_url + f'/{dataset_name}'

    # pridobi filename
    try:
        r = requests.get(catalog_url, verify=False)
        if r.status_code == 200:
            results = r.json()
            file_name = results['data']['datasets'][0]['file_name']
        else:
            flash('Error deleting results (no catalog connection)!')
            return redirect('/')
    except:
        flash('Error deleting results!')
        return redirect('/')

    # izbriši iz baze
    try:
        r_delete = requests.delete(delete_url, verify=False)
    except:
        flash('Error deleting dataset!')
        return redirect('/')

    if r_delete.status_code == 200:
        # izbriši iz  S3
        try:
            storage_url = app.config['STORAGE_URL'] + f'/{dataset_name}'
            response = requests.delete(
                storage_url,
                params={'filename': file_name},
                verify=False
            )
        except:
            flash('Error deleting results (S3 connection)!')
            return redirect('/')

        flash(f'Delete successful: dataset name: {dataset_name}')
    else:
        flash(f'Dataset with name {dataset_name} does not exist!')

    return redirect('/data')





