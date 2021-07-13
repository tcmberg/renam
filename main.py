from flask import Flask, make_response, request, render_template, redirect, url_for, session, send_file, after_this_request
from werkzeug.utils import secure_filename
import tempfile
#from processing import process_data
import pandas as pd
import csv
import os
import zipfile
import shutil
import re
import glob
import urllib,json
import os
import random

from flask_dropzone import Dropzone

import errno, stat

app = Flask(__name__)

dropzone = Dropzone(app)

app.secret_key = 'xyz'

#app.debug = True
#app.config["DEBUG"] = True

#FOlDERS
USER_1 = './USER_1'
USER = USER_1
CSV_FOLDER = os.path.join(USER + '/csv/')
UPLOAD_FOLDER = os.path.join(USER +'/images/')
ALLOWED_EXTENSIONS = set(['zip'])
TEST = os.path.join(USER +'/TEST/')

MAIN_FOLDER = './'
CLEAN_FOLDER = '/home/sofzone/'
DOWNLOAD_FOLDER = '/home/sofzone/USER_1/csv/'


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    foldernames()
    return render_template('image_dropzone.html')

@app.route('/clean', methods=['GET', 'POST'])
def clean_everything():
    alertmessage = deletenames()
    foldernames()
    return render_template('image_dropzone.html', alertmessage=alertmessage)
    #return render_template('image_dropzone.html')




@app.route('/step2', methods=['GET', 'POST'])
def testing_html():
    try:
        for filename in os.listdir(MAIN_FOLDER):
            path_zip = os.path.join(MAIN_FOLDER + filename)
            if '.zip' in filename and not 'images_' in filename:
                zip_ref = zipfile.ZipFile(os.path.join(MAIN_FOLDER, filename), 'r')

                with zip_ref as zip:
                    for zip_info in zip.infolist():
                        if zip_info.filename[-1] == '/':
                            continue
                        zip_info.filename = os.path.basename(zip_info.filename)
                        zip.extract(zip_info, TEST)
                    zip_ref.close()
                    os.remove(path_zip)

                for filename in os.listdir(TEST):
                    filename_or = os.path.splitext(filename)[0]
                    extension = os.path.splitext(filename)[1]

                    or_lower = filename_or.lower() + extension.lower()
                    src = os.path.join(TEST, filename)
                    dst = os.path.join(TEST, or_lower)

                    shutil.move(src,dst)

                return render_template('upload-2.html')
        else:
            alertmessage = 'no zip found'
            #print(alertmessage)
            #return render_template('upload-2.html')
            return render_template('image_dropzone.html', alertmessage=alertmessage)

    except Exception as e:
        print(e)
        info = e
        print('An error occurred.')
        return render_template('image_dropzone.html', info=info)

    return render_template('image_dropzone.html')


# def set_front_or_back_images():
#     if request.method == 'GET':
#         return render_template('step2.html')
#     elif request.method == 'POST':
#             set_front_images = request.form.get('ffolder')
#             print(set_front_images)
#
#     return render_template('step2.html')


@app.route('/step3', methods=["GET", "POST"])
def uploadfile():

    if request.method == 'GET':
        return render_template('upload-2.html')
    elif request.method == 'POST':
        input_file = request.files["input_file"]


        df = pd.read_excel(input_file)
        df = df[df.columns.drop(list(df.filter(regex='koop|description|lengte|Unnamed|harmonised|btw|brand|merk|cuntry|packed|delivery|verzending')))]
        pd.set_option('precision', 0)

        df.to_csv(CSV_FOLDER + 'compare.csv', sep=',', encoding='utf-8', index=False, header=True, float_format='%g')
        df.to_csv(CSV_FOLDER + 'original.csv', sep=',', encoding='utf-8', index=False, header=True, float_format='%g')
        images = [x for x in os.listdir(TEST)[:10]]
        return render_template('upload-2.html', tables=[df.to_html(classes='data', max_rows=15)], titles=df.columns.values, data=images)


def setup_front_images(set_front_images):
    if set_front_images == 'set_front_images':
        image_code = '115'
    elif set_front_images == 'set_back_images':
        image_code = '719'
    else:
        image_code = ''
    return image_code


def cleanup_list():
    try:
        for filename in os.listdir(TEST):
            if not filename.startswith('8712265000'):
                print(f'remove {filename}')
                filename = os.path.join(TEST, filename)
                os.remove(filename)

    except:
        print('.')
    return 'cleanup'

def zip_file_finder():
    try:
        for filename in os.listdir(MAIN_FOLDER):
            if filename.startswith('images_'):
                return filename
    except:
        print('.')
    return 'zip_file_downloader'



@app.route('/step4', methods=['GET', 'POST'])
def nextgen():
        if request.method == 'GET':
            return render_template('/upload.html')
        elif request.method == 'POST':

            input_gtin = request.form.get('gtin_in')
            input_1 = request.form.get('input_1')
            input_2 = request.form.get('input_2')

            set_front_images = request.form.get('ffolder')
            image_code = setup_front_images(set_front_images)
        #   print(image_code)
            pd.set_option('precision', 0)

            col_list = [input_gtin, input_1, input_2]
            db2 = pd.read_csv(CSV_FOLDER + 'compare.csv', delimiter=',', usecols=col_list, converters={input_1: lambda x: '{0:0>3}'.format(x).lower(), input_2: lambda x: '{0:0>2}'.format(x).lower()})

            db2[input_gtin] = db2[input_gtin].round().astype('Int64')

            db2.sort_values(input_1, ascending=True)
            db1 = db2.drop_duplicates(subset=[input_1])



            csv_filename = 'compare.csv'
            csv_fullname = os.path.join(CSV_FOLDER, csv_filename)

            db1.to_csv(csv_fullname, sep=',', encoding='utf-8', columns=col_list, index=False, header=True)

            front_bitches(input_gtin, input_1, input_2, image_code)

            cleanup_list()
            imagecount = len([x for x in os.listdir(TEST)])
            shutil.make_archive('images_' + str(random.randint(0, 999)), 'zip', TEST, MAIN_FOLDER)
            shutil.rmtree(TEST)
            print(imagecount)

            db_out = pd.read_csv(CSV_FOLDER + 'back_output.csv', delimiter=',')
            db_out_dup = db_out.drop_duplicates(subset=["EAN"])

        #    return render_template('thank-you.html', imagecount=imagecount)
            return render_template('thank-you.html', imagecount=imagecount, tables=[db_out_dup.to_html(classes='data')], titles=db_out_dup.columns.values)


@app.route('/download_images.html', methods=["GET", "POST"])
def download_images():
    filename_zipper = zip_file_finder()
    path = os.path.join(CLEAN_FOLDER + filename_zipper)
    return send_file(path, as_attachment=True, cache_timeout=0)

@app.route('/download_csv.html', methods=["GET", "POST"])
def download_csv():
    csv_filename = 'back_output.csv'
    csv_fullname = os.path.join(CSV_FOLDER, csv_filename)
    return send_file(csv_fullname, as_attachment=True, cache_timeout=0)





def front_bitches(input_gtin, input_1, input_2, image_code):
    print('start renaming')
    try:
        with open(CSV_FOLDER + 'compare.csv') as f, open(CSV_FOLDER + 'back_output.csv', 'w') as b_output:
            reader = csv.reader(f, delimiter=',')
            writer_back = csv.writer(b_output)
            writer_back.writerow(['EAN', input_1, input_2])
            next(reader)

            image_code = image_code
            #print(image_code)

            for row in reader:
                gtin = row[0]
                input1 = row[1].lower()
                input2 = row[2].lower()

                for filename in os.listdir(TEST):
                    extension = os.path.splitext(filename)[1]
                    if input1 in filename and input2 in filename:
                        #print(f'image: {filename} ==> MATCH WITH {input1} and {input2} ')
                        #print(image_code)
                        rename_string = '8712265000' + image_code + gtin + extension
                        old_file_loc = os.path.join(TEST, filename)
                        new_file_loc = os.path.join(TEST, rename_string)
                        writer_back.writerow(row)
                        os.replace(old_file_loc, new_file_loc)
                        continue
    except Exception as e:
        print(e)
        info = e
        print(f'An error occurred. {info}')

    return 'done processing back images'


def foldernames():
    if not os.path.exists(CSV_FOLDER):
        os.makedirs(CSV_FOLDER)
        print('CSV_FOLDER folder created.')
    if not os.path.exists(TEST):
        os.makedirs(TEST)
        print('TEST folder created.')


def deletenames():
    try:
        for filename in os.listdir(MAIN_FOLDER):
            if filename.startswith('images_'):
                alertmessage = 'image zip removed!'
                os.remove(filename)
                return alertmessage
            else:
                alertmessage = 'no image zipfile found'
                return alertmessage

    except Exception as e:
        print(e)
        info = e
        print(f'An error occurred. {info}')


if __name__ == '__main__':
    app.run(debug=False)
