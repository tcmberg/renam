from flask import Flask, make_response, request, render_template, redirect, url_for, session, send_file, after_this_request
from werkzeug.utils import secure_filename
#import tempfile
#from processing import process_data
import pandas as pd
import csv
import os
import zipfile
import shutil
import re

from flask_dropzone import Dropzone


import errno, stat

app = Flask(__name__)

dropzone = Dropzone(app)

app.secret_key = 'xyz'

#app.debug = True
#app.config["DEBUG"] = True

CSV_FOLDER = './var/www/temp/output_list.csv'
UPLOAD_FOLDER = './var/www/temp/images/'
SUCCESS_F = './var/www/temp/success/f/'
SUCCESS_B = './var/www/temp/success/b/'
ALLOWED_EXTENSIONS = set(['zip'])
front_folder = './var/www/temp/images/front_images/'
back_folder = './var/www/temp/images/back_images/'
image_container = './var/www/temp/image/image_container/'
MAIN_FOLDER = './'

print(MAIN_FOLDER)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def root_htmlzaio():


    for filename in os.listdir(MAIN_FOLDER):
        path_zip = os.path.join(MAIN_FOLDER + filename)
        if '.zip' in filename:
            os.remove(path_zip)


    return render_template('image_dropzone.html')

@app.route('/testing', methods=['GET', 'POST'])
def testing_html():
    foldernames()
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            zip_ref = zipfile.ZipFile(os.path.join(UPLOAD_FOLDER, filename), 'r')
            zip_ref.extractall(UPLOAD_FOLDER)
            zip_ref.close()
            image_list = []
            i = 0
            for filename in os.listdir(UPLOAD_FOLDER):
                filename_or = os.path.splitext(filename)[0]
                extension = os.path.splitext(filename)[1]
                clean_name = re.sub("[^a-zA-Z0-9_]", "", filename_or).lower() + extension.lower()

                #print(clean_name, extension)
                #print(lower(clean_name))

                src = os.path.join(UPLOAD_FOLDER, filename)
                dst = os.path.join(UPLOAD_FOLDER, clean_name)
                #os.rename(src, dst)
                shutil.move(src,dst)
                img_container = os.path.join(image_container, clean_name)
                image_list.append(clean_name)
                #print(img_container)
                if '.jpg' in clean_name or '.png' in clean_name:
                    shutil.copyfile(dst, img_container)
            #print(image_list)
                #shutil.copy(dst, image_container)


        #return render_template('image_.html')
            session['image_list'] = image_list
            return render_template('image_processed.html', data=image_list)

@app.route('/continue')
def continue_html():
    return render_template('image_processed.html', data=session['image_list'])

@app.route('/imagename', methods=['GET', 'POST'])
def frontbackimages():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        suffix = request.form.get('back_images')
        rename_front(suffix)
        #totalrenamer(suffix)
        return redirect('/upload.html')

    #return redirect('/process.html')
    return render_template('/index.html')

def foldernames():
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
        print('front folder created.')
    if not os.path.exists(image_container):
        os.makedirs(image_container)
        print('front folder created.')
    if not os.path.exists(front_folder):
        os.makedirs(front_folder)
        print('front folder created.')
    if not os.path.exists(back_folder):
        os.makedirs(back_folder)
        print('back folder created.')
    if not os.path.exists(SUCCESS_F):
        os.makedirs(SUCCESS_F)
        print('SUCCESS_F folder created.')
    if not os.path.exists(SUCCESS_B):
        os.makedirs(SUCCESS_B)
        print('SUCCESS_B folder created.')

@app.route('/imagename', methods=['GET', 'POST'])
def rename_front(suffix):
    #foldernames()
    param = suffix
    my_file = CSV_FOLDER
    #print(UPLOAD_FOLDER)
    #suffix = param
    for filename in os.listdir(image_container):
        or_name = os.path.splitext(filename)[0]
        front_image_list = []
        back_image_list = []
        #print(param)
        if param in or_name[-4:]:
            src = os.path.join(image_container, filename)
            dst_source = os.path.join(back_folder, filename)
            shutil.copyfile(src, dst_source)
            #shutil.copyfile(src, dst_source)
            #print(src, dst_source)
        else:
            src = os.path.join(image_container, filename)
            dst_source = os.path.join(front_folder, filename)
            #print(f'not greater {src}, {dst_source}')
            shutil.copyfile(src, dst_source)
    return front_image_list



@app.route('/upload.html', methods=["GET", "POST"])
def uploadfile():

    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        input_file = request.files["input_file"]
        df = pd.read_excel(input_file, delimiter=',')

        df.to_csv('./var/www/temp/' + 'test.csv', sep=',', encoding='utf-8', index=False, header=True)
        #test(df)
        #return render_template('upload.html')
        images = [x for x in os.listdir(image_container)[:3]]
        return render_template('upload.html', tables=[df.to_html(classes='data', max_rows=3)], titles=df.columns.values, data=images)


@app.route('/upload2.html', methods=["GET", "POST"])
def test():

    if request.method == 'GET':
        return render_template('/upload.html')
    elif request.method == 'POST':

        input_gtin = request.form.get('gtin_in')
        input_1 = request.form.get('input_1')
        input_2 = request.form.get('input_2')
        col_list = [input_gtin, input_1, input_2]

        database2 = pd.read_csv('./var/www/temp/' + 'test.csv', delimiter=',', usecols=col_list, converters={input_1: lambda x: '{0:0>4}'.format(x).lower(), input_2: lambda x: '{0:0>3}'.format(x).lower()})
        database2.sort_values(input_1, ascending=True)
        database2.drop_duplicates(subset=[input_1])
        df_update = database2.replace(to_replace="[^a-zA-Z0-9_]", value="",regex=True)
        #print(df_update)
        df_update.to_csv('./var/www/temp/' + 'test.csv', sep=',', encoding='utf-8', columns=col_list, index=False, header=False)



        with open('./var/www/temp/' + 'test.csv') as f, open('./var/www/temp/' + 'output_list.csv', 'w', newline='') as f_out:
            reader = csv.reader(f, delimiter=',')
            writer = csv.writer(f_out, delimiter=',')

            new_list = []
            gtin_list = []
            for row in reader:
                gtin = row[0]
                input1 = row[1]
                input2 = row[2]
                for filename in os.listdir(front_folder):
                    extension = os.path.splitext(filename)[1]
                    if input1 in filename and input2 in filename:
                        #print(f'hello this is crazy: {filename}, {gtin}, {input1}, {input2} ')
                        src = os.path.join(front_folder, filename)
                        #dstfile = input1 + '_' + input2 + '_front' + extension
                        f_rename = '8712265000' + '115' + gtin + extension
                        dst = os.path.join(SUCCESS_F, f_rename)
                        #os.rename(src, dst)
                        shutil.move(src, dst)
                    else:
                        continue

                for filename in os.listdir(back_folder):
                    extension = os.path.splitext(filename)[1]
                    #print(f'hello this is weird: {filename}, {gtin}, {input1}, {input2} ')
                    if input1 in filename and input2 in filename:
                        #print(f'hello this is crazy: {filename}, {gtin}, {input1}, {input2} ')
                        src = os.path.join(back_folder, filename)
                        #dstfile = input1 + '_' + input2 + '_back' + extension
                        b_rename = '8712265000' + '719' + gtin + extension
                        dst = os.path.join(SUCCESS_B, b_rename)
                        #os.rename(src, dst)
                        shutil.move(src, dst)
                    else:
                        continue


        shutil.make_archive('front_images', 'zip', SUCCESS_F)
        shutil.make_archive('back_images', 'zip', SUCCESS_B)
        shutil.rmtree(front_folder)
        shutil.rmtree(back_folder)
        shutil.rmtree(image_container)
        shutil.rmtree(UPLOAD_FOLDER)
        shutil.rmtree(SUCCESS_F)
        shutil.rmtree(SUCCESS_B)
            #writer.writerows(zip(new_list, gtin_list))


        return render_template('/thank-you.html')


@app.route('/download-front.html', methods=["GET", "POST"])
def download_front_images():
    zip = 'front_images.zip'
    path = os.path.join(MAIN_FOLDER + zip)

    return send_file(path, as_attachment=True)

@app.route('/download-back.html', methods=["GET", "POST"])
def download_back_images():
    zip ='back_images.zip'
    path = os.path.join(MAIN_FOLDER + zip)

    return send_file(path, as_attachment=True)




if __name__ == '__main__':
    app.run(debug=False)
