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
SUCCESS_F =  os.path.join(USER + '/success/f/')
SUCCESS_B =  os.path.join(USER + '/success/b/')
ALLOWED_EXTENSIONS = set(['zip'])
front_folder =  os.path.join(USER + '/front_images/')
back_folder =  os.path.join(USER + '/back_images/')
image_container =  os.path.join(USER + '/image/image_container/')


MAIN_FOLDER = './'
CLEAN_FOLDER = '/home/sofzone/'







def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/')
def root_htmlzaio():


    try:
        for filename in os.listdir(CLEAN_FOLDER):
            if 'back_images.zip' in filename or 'front_images.zip' in filename:
                os.remove(filename)

    except:
        print('All cleaned up!')

    try:
        if os.path.exists(USER_1):
            shutil.rmtree(USER_1)
    except:
        print('nothing to see')

    return render_template('image_dropzone.html')


@app.route('/go', methods=['GET', 'POST'])
def testing_html():
    foldernames()

    try:
        for filename in os.listdir(MAIN_FOLDER):
            path_zip = os.path.join(MAIN_FOLDER + filename)
            if '.zip' in filename:

                zip_ref = zipfile.ZipFile(os.path.join(MAIN_FOLDER, filename), 'r')
                #zip_ref.extractall(UPLOAD_FOLDER)
                #zip_ref.close()
                #os.remove(path_zip)
                #image_list = []

                with zip_ref as zip:
                    for zip_info in zip.infolist():
                        if zip_info.filename[-1] == '/':
                            continue
                        zip_info.filename = os.path.basename(zip_info.filename)
                        zip.extract(zip_info, UPLOAD_FOLDER)
                    zip_ref.close()
                    os.remove(path_zip)
                    image_list = []

                #ZIP FILE > ORGANIZE

                for filename in os.listdir(UPLOAD_FOLDER):
                        filename_or = os.path.splitext(filename)[0]
                        extension = os.path.splitext(filename)[1]
                        clean_name = re.sub("[^a-zA-Z0-9_]", "", filename_or).lower() + extension.lower()

                        src = os.path.join(UPLOAD_FOLDER, filename)
                        dst = os.path.join(UPLOAD_FOLDER, clean_name)

                        shutil.move(src,dst)
                        img_container = os.path.join(image_container, clean_name)
                        image_list.append(clean_name)

                        #all images that are moved to container.


                        if '.jpg' in clean_name or '.png' in clean_name:
                            shutil.move(dst, img_container)
                            #count_move_images = count_move_images + 1


                        #shutil.rmtree(UPLOAD_FOLDER)

                #session['image_list'] = image_list
                #return render_template('image_processed.html', data=image_list)

                shutil.rmtree(UPLOAD_FOLDER)
                return render_template('image_processed.html')


    except:
        print('An error occurred.')
        return render_template('image_dropzone.html')

    return render_template('image_dropzone.html')

@app.route('/continue')
def continue_html():

    #return render_template('image_processed.html', data=session['image_list'])
    return render_template('image_processed.html')

@app.route('/imagename', methods=['GET', 'POST'])
def frontbackimages():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        suffix = request.form.get('back_images')
        fsuffix = request.form.get('front_images')
        rename_front(suffix, fsuffix)
        #totalrenamer(suffix)
        return redirect('/upload.html')

    #return redirect('/process.html')
    return render_template('image_dropzone.html')



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
    if not os.path.exists(CSV_FOLDER):
        os.makedirs(CSV_FOLDER)
        print('CSV_FOLDER folder created.')



@app.route('/imagename', methods=['GET', 'POST'])
def rename_front(suffix, fsuffix):
    param = suffix
    fparam = fsuffix
    #print(f'{fparam} this is front param')

    for filename in os.listdir(image_container):
        or_name = os.path.splitext(filename)[0]

        if param in or_name:

            src = os.path.join(image_container, filename)
            dst_source = os.path.join(back_folder, filename)
            shutil.move(src, dst_source)
            #os.remove(image_container, filename)

        elif fparam in or_name:
            src = os.path.join(image_container, filename)
            dst_source = os.path.join(front_folder, filename)
            shutil.move(src, dst_source)
        else:
            print('no match')

        # else:

        #     src = os.path.join(image_container, filename)
        #     dst_source = os.path.join(front_folder, filename)
        #     shutil.copyfile(src, dst_source)
        #     #os.remove(image_container, filename)



    front_count = len(os.listdir(front_folder))
    back_count = len(os.listdir(back_folder))
    print(f'front images count: {front_count}, back images count: {back_count}')

    #uploadfile(front_count, back_count)
    return render_template('upload.html')



@app.route('/upload.html', methods=["GET", "POST"])
def uploadfile():

    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        input_file = request.files["input_file"]
        #input_file = request.form.get("input_file")
        df = pd.read_excel(input_file, delimiter=',')
        df = df[df.columns.drop(list(df.filter(regex='koop|omschrijv|description|lengte|Unnamed|harmonised|btw')))]

        df.to_csv(CSV_FOLDER + 'test.csv', sep=',', encoding='utf-8', index=False, header=True)
        original_df = df
        original_df.to_csv(CSV_FOLDER + 'original.csv', sep=',', encoding='utf-8', index=False, header=True)
        #df.to_csv('./var/www/temp/' + 'test.csv', sep=',', encoding='utf-8', index=False, header=True)
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

        database2 = pd.read_csv(CSV_FOLDER + 'test.csv', delimiter=',', usecols=col_list, converters={input_1: lambda x: '{0:0>4}'.format(x).lower(), input_2: lambda x: '{0:0>3}'.format(x).lower()})
        database2.sort_values(input_1, ascending=True)
        database2.drop_duplicates(subset=[input_1])
        df_update = database2.replace(to_replace="[^a-zA-Z0-9_]", value="",regex=True)
        #print(df_update)
        csv_filename = 'test.csv'
        csv_fullname = os.path.join(CSV_FOLDER, csv_filename)
        df_update.to_csv(csv_fullname, sep=',', encoding='utf-8', columns=col_list, index=False, header=True)

        #df_update.to_csv('./var/www/temp/' + 'test.csv', sep=',', encoding='utf-8', columns=col_list, index=False, header=False)



        with open(CSV_FOLDER + 'test.csv') as f, open(CSV_FOLDER + 'output.csv', 'w') as b:
            reader = csv.reader(f, delimiter=',')

            writer = csv.writer(b)
            writer.writerow([input_gtin, input_1, input_2, 'gedaan'])
            next(reader)


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
                        writer.writerow(row+['gedaan'])
                        shutil.move(src, dst)
                    else:
                        writer.writerow(row+['niet gedaan'])
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
                        writer.writerow(row+['gedaan'])
                    else:
                        writer.writerow(row+['niet gedaan'])
                        continue


        fs = pd.read_csv(CSV_FOLDER + 'output.csv', delimiter=',')
        fs3 = fs.drop_duplicates(keep=False, inplace=True)

        custom_columns = [input_gtin]
        custom_columns.append('gedaan')
        #print(custom_columns)
        fs3.to_csv(CSV_FOLDER + 'output3.csv', sep=',', encoding='utf-8', index=False, header=True, columns=custom_columns)
        fs3.close()


        fs2 = pd.read_csv(CSV_FOLDER + 'output3.csv', delimiter=',')
        oxo = pd.read_csv(CSV_FOLDER + 'original.csv', delimiter=',')

        exam_scores = oxo.merge(fs2, on=input_gtin)

        best_original = pd.concat([oxo,exam_scores]).drop_duplicates().reset_index(drop=True)
        print(best_original)
        best_original.to_excel(CSV_FOLDER + 'output2.xlsx', sheet_name='check_sheet', encoding='utf-8', index=False, header=True)

        #oxo = pd.read_csv(CSV_FOLDER + 'original.csv', delimiter=',')
        #scores = fs.merge(oxo, on=input_gtin)
        #dd.to_csv(CSV_FOLDER + 'output.csv', sep=',', encoding='utf-8', index=False, header=True)
        #print(dd.head())
        #print(dd)

        #oxo.merge(fs, on=input_gtin, how='left')
        #print(oxo)
        #oxo.to_csv(CSV_FOLDER + 'john.csv', sep=',', encoding='utf-8', index=False, header=True)

        #print(fs)

        shutil.make_archive('front_images', 'zip', SUCCESS_F, MAIN_FOLDER)
        shutil.make_archive('back_images', 'zip', SUCCESS_B, MAIN_FOLDER)
        shutil.rmtree(front_folder)
        shutil.rmtree(back_folder)
        shutil.rmtree(image_container)
    #    shutil.rmtree(UPLOAD_FOLDER)
        shutil.rmtree(SUCCESS_F)
        shutil.rmtree(SUCCESS_B)


        return render_template('/thank-you.html')


@app.route('/download-front.html', methods=["GET", "POST"])
def download_front_images():

    zip = 'front_images.zip'
    path = os.path.join(CLEAN_FOLDER + zip)

    return send_file(path, as_attachment=True, cache_timeout=0)

@app.route('/download-back.html', methods=["GET", "POST"])
def download_back_images():
    zip = 'back_images.zip'
    path = os.path.join(CLEAN_FOLDER + zip)

    return send_file(path, as_attachment=True, cache_timeout=0)

@app.route('/download-csv.html', methods=["GET", "POST"])
def download_excel_file():
    csv_file = 'output2.xlsx'
    path = os.path.join('/USER_1/csv/' + csv_file)

    return send_file(path, as_attachment=True, cache_timeout=0)


if __name__ == '__main__':
    app.run(debug=True)
