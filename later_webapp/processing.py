from flask import Flask, make_response, request, redirect, render_template
import os
import csv
import pandas
from werkzeug.utils import secure_filename
import tempfile

app = Flask(__name__)

#@app.route("/upload", methods=["GET", "POST"])

@app.route("/output")
def process_data(input_file):

    my_file = input_file
    col_list = ['hoofdkleur', 'merk']
    tf = tempfile.NamedTemporaryFile()
    df = pandas.read_csv(my_file, delimiter=',', usecols=col_list)
    df.to_csv('./var/www/temp/' + secure_filename(tf.name), sep=',', encoding='utf-8', columns=col_list, index=False, header=False)
    return render_template('/output.html', tables=[df.to_html(classes='data')], titles=df.columns.values)
    #return redirect('/output')
    #return 'file uploaded'
