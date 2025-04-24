# Utility script used to convert xml data to csv files

import pandas as pd
import xml.etree.ElementTree as ET
import os



dataset_path = "F:/Università/x.Magistrale/Primo_Anno\Machine Learning/Progetto/Datasets/GMAPSCT/dataset"


tree = ET.parse(os.path.join(dataset_path, "coordinates.xml"))
root = tree.getroot()


metadata = []
for entry in root.findall('entry'):
    id = entry.get('id')


    tree = ET.parse(os.path.join(dataset_path, "labels - PASCAL VOC", id + ".xml"))
    root = tree.getroot()
    width = root.find('size').find('width').text
    height = root.find('size').find('height').text


    longitude = entry.find('longitude').text
    latitude = entry.find('latitude').text
    zoom = entry.find('zoom').text
    heading = entry.find('heading').text
    tilt = entry.find('tilt').text
    metadata.append([id, longitude, latitude, zoom, heading, tilt, width, height])

metadata_df = pd.DataFrame(metadata, columns=['id', 'longitude', 'latitude', 'zoom', 'heading', 'tilt', 'width', 'height'])
metadata_df['id'] = metadata_df['id'].astype(int)
metadata_df['longitude'] = metadata_df['longitude'].astype(float)
metadata_df['latitude'] = metadata_df['latitude'].astype(float)
metadata_df['zoom'] = metadata_df['zoom'].astype(float)
metadata_df['heading'] = metadata_df['heading'].astype(float)
metadata_df['tilt'] = metadata_df['tilt'].astype(float)
metadata_df['width'] = metadata_df['width'].astype(float)
metadata_df['height'] = metadata_df['height'].astype(float)
metadata_df.to_csv(os.path.join(dataset_path, "coordinates.csv"), index=False)

print("metadata.csv created")


#create labels.csv
labels = []
for filename in os.listdir(os.path.join(dataset_path, "labels - PASCAL VOC")):
    if filename.endswith(".xml"):
        tree = ET.parse(os.path.join(dataset_path, "labels - PASCAL VOC", filename))
        root = tree.getroot()
        id = filename.split(".")[0]


        for obj in root.findall('object'):
            name = obj.find('name').text
            bndbox = obj.find('bndbox')
            xmin = bndbox.find('xmin').text
            ymin = bndbox.find('ymin').text
            xmax = bndbox.find('xmax').text
            ymax = bndbox.find('ymax').text
            labels.append([id, name, xmin, ymin, xmax, ymax])

            #print("obj info", id, name, xmin, ymin, xmax, ymax)
        



#store in dataset_path as labels.csv
labels_df = pd.DataFrame(labels, columns=['id', 'name', 'xmin', 'ymin', 'xmax', 'ymax'])
labels_df['id'] = labels_df['id'].astype(int)
labels_df['name'] = labels_df['name'].astype(str)
labels_df['xmin'] = labels_df['xmin'].astype(float)
labels_df['ymin'] = labels_df['ymin'].astype(float)
labels_df['xmax'] = labels_df['xmax'].astype(float)
labels_df['ymax'] = labels_df['ymax'].astype(float)
labels_df.to_csv(os.path.join(dataset_path, "labels.csv"), index=False)

print("labels.csv created")
