import csv
import os
import re
import pandas as pd

def test_images_function():
    #CURR_DIR = os.getcwd()
    IMAGE_TEST = os.getcwd() + "/TEST_IMAGES/"
    list_images = []
    for i in os.listdir(IMAGE_TEST):
        i = os.path.splitext(i)[0]
        i = re.sub('[^a-zA-Z0-9 \n\.\.]', ',', i)
        i = re.sub('[ ,.]', ',', i)
        list_images.append(i.split(','))



    return list_images
        #print(list_images)





def checker():
    CURR_DIR = os.getcwd()

    list_images = test_images_function()
#    print(list_images)
    print('####################################################################################')
    print('####################################################################################')
    print('Starting up..')
    print('####################################################################################')
    print('####################################################################################')

    #IMAGES TO CSV
    with open(CURR_DIR + '/images_file.csv', 'w') as f:
        image_writer = csv.writer(f, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        image_writer.writerows(list_images)
        #image_writer.writerows(list_images)

    #CSV REGEX FIX
    with open(CURR_DIR + '/tsst.csv') as f, open(CURR_DIR + '/fix_file.csv', 'w') as w:
        data_file = csv.reader(f, delimiter=' ', quotechar=',')
        data_writer = csv.writer(w, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
        next(data_file)
        #l = [item.lower() for item in f]
        list_data = []
        for row in f:
            row.lower()
            row = re.sub('[^a-zA-Z0-9 \n\.\.]', ',', row)
            row = re.sub('[ ,.]', ',', row)
            list_data.append(row.split(','))
        #    print(row)
        #print(list_data)
#

        data_writer.writerows(list_data)
        #print(row)



    print('####################################################################################')
    print('####################################################################################')




def comparing_files():
    #checker()
    CURR_DIR = os.getcwd()
    lines = open(CURR_DIR + '/fix_file.csv', 'r').read()

    #print(lines)
    with open(CURR_DIR + '/images_file.csv', 'r') as master, open(CURR_DIR + '/fix_file.csv', 'r') as hosts:
        r1 = csv.reader(master)
        r2 = csv.reader(hosts)

        master_list = list(r1)
        hosts_list = list(r2)

        df1 = pd.DataFrame(master_list)
        df2 = pd.DataFrame(hosts_list)

        df1 = df1.sort_values(by=0)
        df1 = df1.dropna(thresh=5)
        df1 = df1.dropna(axis=1, thresh=None)

        #print(df1)
        df2 = df2.sort_values(by=0)
        df2 = df2.dropna(thresh=40)
        df2 = df2.dropna(axis=1, thresh=None)

        #print(df2.items)

        df1.to_csv('image_names.csv', index=False)
        df2.to_csv('items_from_excel.csv', index=False)



comparing_files()
