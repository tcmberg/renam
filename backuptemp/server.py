from flask import Flask, make_response, request, render_template, redirect, url_for
from werkzeug.utils import secure_filename
#import tempfile
#from processing import process_data
import pandas as pd
import csv
import os
import zipfile
import shutil

app = Flask(__name__)
#app.debug = True
#app.config["DEBUG"] = True

CSV_FOLDER = './var/www/temp/output_list.csv'
UPLOAD_FOLDER = './var/www/temp/images/'
ALLOWED_EXTENSIONS = set(['zip'])
front_folder = './var/www/temp/images/front_images/'
back_folder = './var/www/temp/images/back_images/'



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=["GET", "POST"])
def root():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        input_file = request.files["input_file"]
        df = pd.read_csv(input_file, delimiter=',')
        df.to_csv('./var/www/temp/' + 'test.csv', sep=',', encoding='utf-8', index=False, header=True)
        return render_template('upload.html', tables=[df.to_html(classes='data', max_rows=3)], titles=df.columns.values)


@app.route('/input', methods=["GET", "POST"])
def test():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        input_gtin = request.form.get('gtin_in')
        input_sku = request.form.get('sku_in')
        input_color = request.form.get('color_in')
        input_extra = request.form.get('extra_in')

        prefix = request.form.get('prefix')
        suffix2 = request.form.get('suffix2')
        suffix3 = request.form.get('suffix3')

        col_list = [input_gtin, input_sku, input_color, input_extra]

        database2 = pd.read_csv('./var/www/temp/' + 'test.csv', delimiter=',', usecols=col_list, converters={input_color: lambda x: str(x), input_extra: lambda x: str(x)})
        database2.sort_values(input_sku, ascending=True)
        database2.drop_duplicates(subset=[input_sku])
        database2.to_csv('./var/www/temp/' + 'test.csv', sep=',', encoding='utf-8', columns=col_list, index=False, header=False)

        with open('./var/www/temp/' + 'test.csv') as f, open('./var/www/temp/' + 'output_list.csv', 'w', newline='') as f_out:
            reader = csv.reader(f, delimiter=',')
            writer = csv.writer(f_out, delimiter=',')

            new_list = []
            gtin_list = []

            for row in reader:
                gtin = row[0]
                sku = row[1]
                colorgroup = row[2]
                extra = row[3]

                imagenamed = str(prefix) + sku + str(suffix2) + colorgroup + str(suffix3) + extra
                new_list.append(imagenamed)
                gtin_list.append(gtin)
                #print(row)
                #writer.writerow(imagenamed)
            writer.writerows(zip(new_list, gtin_list))

        return redirect('/index.html')

@app.route('/index.html', methods=['GET', 'POST'])
def upload_file():
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

            i = 0
            for filename in os.listdir(UPLOAD_FOLDER):
                replacement = filename.replace('.JPG', '.jpg')
                replacement2 = filename.replace(' kopie', '')
                src = UPLOAD_FOLDER + filename
                dst = UPLOAD_FOLDER + replacement2
                os.rename(src, dst)
            return redirect('index.html')
    return render_template('index.html')

@app.route('/imagename', methods=['GET', 'POST'])
def frontbackimages():
    if request.method == 'GET':
        return render_template('index.html')
    elif request.method == 'POST':
        suffix = [request.form.get('front_images'), request.form.get('back_images')]
        rename_front(suffix)
        totalrenamer(suffix)

    #return redirect('/process.html')
    return render_template('index.html')

@app.route('/imagename', methods=['GET'])
def rename_front(suffix):
    param = suffix
    my_file = CSV_FOLDER
    #print(UPLOAD_FOLDER)
    #suffix = param
    foldernames()

    try:
        for filename in os.listdir(UPLOAD_FOLDER):
            or_name = os.path.splitext(filename)[0]
            front_image_list = []
            back_image_list = []

            if param[0] in or_name[-4:]:
                src = UPLOAD_FOLDER + filename
                dst_source = front_folder + filename
                #print(param[1], or_name)
                front_image_list.append(filename)
                #print(frontimage_list)
                #print(src, dst_source)
                shutil.copyfile(src, dst_source)

            elif param[1] in or_name[-4:]:
                src = UPLOAD_FOLDER + filename
                dst_source = back_folder + filename
                back_image_list.append(filename)
                shutil.copyfile(src, dst_source)

            else:
                continue

        shutil.make_archive('front_images', 'zip', front_folder)
        #shutil.rmtree(front_images_folder)
        return totalrenamer()
    except:
        return 'fails'


def totalrenamer(suffix):
    param = suffix
    # front_folder new image location
    #print(param[0])


    try:
        for filename in os.listdir(front_folder):
            extension = os.path.splitext(filename)[1]
            f_or_name = os.path.splitext(filename)[0]
            src = front_folder + filename
            with open(CSV_FOLDER) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                #print(csv_file)
                for row in csv_reader:

                    csv_f_filenames = row[0] + param[0]



                    if csv_f_filenames == f_or_name:
                        f_rename = '8712265000' + '115' + row[1] + extension
                        dst = front_folder + f_rename
                        os.rename(src, dst)

                    else:
                        continue
    except:
        return 'error'

    try:
        for filename in os.listdir(back_folder):
            extension = os.path.splitext(filename)[1]
            b_or_name = os.path.splitext(filename)[0]
            src = front_folder + filename
            with open(CSV_FOLDER) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                #print(csv_file)
                for row in csv_reader:
                    csv_b_filenames = row[0] + param[1]
                    if csv_b_filenames == b_or_name:
                        #print('f_yes')
                        b_rename = '8712265000' + '719' + row[1] + extension
                        dst = front_folder + f_rename
                        os.rename(src, dst)

                    else:
                        continue

        shutil.make_archive('back_images', 'zip', back_folder)
    except:
        return 'error'





def foldernames():
    if not os.path.exists(front_folder):
        os.makedirs(front_folder)
        print('front folder created.')
    if not os.path.exists(back_folder):
        os.makedirs(back_folder)
        print('back folder created.')



if __name__ == '__main__':
    app.run(debug=True)


# # @app.route('/', methods=["GET", "POST"])
# # def indexpage():
# #     return render_template('upload.html')
#
#
# @app.route("/", methods=["GET", "POST"])
# def uploadfiles():
#     if request.method == "POST":
#         #tf = tempfile.NamedTemporaryFile()
#         input_file = request.files["input_file"]
#         output_data = process_data(input_file)
#         print(output_data)
#     return render_template('/upload.html')
#
# @app.route("/output")
# def output():
#     return render_template('output.html')
