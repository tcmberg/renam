from flask import Flask, make_response, request, render_template, redirect
from werkzeug.utils import secure_filename
import tempfile
from processing import process_data
import pandas as pd


app = Flask(__name__)
#app.debug = True
#app.config["DEBUG"] = True


@app.route('/', methods=["GET", "POST"])
def root():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        input_file = request.files["input_file"]
        df = pd.read_csv(input_file, delimiter=',')
        tf = tempfile.NamedTemporaryFile()
        df.to_csv('./var/www/temp/' + secure_filename(tf.name), sep=',', encoding='utf-8', index=False, header=False)
        new_file = './var/www/temp/' + secure_filename(tf.name)
        return render_template('upload.html', tables=[df.to_html(classes='data', max_rows=3)], titles=df.columns.values)

@app.route('/test', methods=['GET', 'POST'])
def test():

    input_gtin = request.form.get('gtin_in')
    input_sku = request.form.get('sku_in')
    input_color = request.form.get('color_in')
    input_extra = request.form.get('extra_in')
    col_list = [input_gtin, input_sku, input_color, input_extra]
    df2 = pd.read_csv(new_file, delimiter=',')
    print(df2)


    return render_template('upload.html', tables=[df2.to_html(classes='data', max_rows=3)], titles=df2.columns.values)



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
