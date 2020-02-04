import json
import os
import csv
import argparse
import collections
import numpy as np
import cv2

dic = { }

parser = argparse.ArgumentParser()
parser.add_argument('path', help='Path of the Target dataset')
args = parser.parse_args()

json_dict = {}
data = []

colonies = ['ADAR', 'AMBU', 'ANDI', 'ANNE', 'ARDL', 'ARMS', 'AUST', 'AVIA', 'BACK',
            'BARC', 'BATT', 'BEAG', 'BEAU', 'BECH', 'BELG', 'BERK', 'BERT', 'BIRD', 'BISC',
            'BRAS', 'BRAT', 'BRDM', 'BRDN', 'BRDS', 'BROW', 'BSON', 'BURK', 'CBAR', 'CHRI',
            'CIOL', 'CONT', 'CROZ', 'CURZ', 'DARB', 'DAVI', 'DEEI', 'DEMS', 'DEVI', 'DURO', 'DUTH',
            'EARL', 'EDMO', 'EDWA', 'ETNA', 'EVEN', 'EVER', 'FERR', 'FISH', 'FRNC', 'GEPT', 'GIBS',
            'GOSL', 'GOUR', 'HANN', 'HBAY', 'HERO', 'HOLD', 'HOLL', 'HOPE', 'IFOI', 'IVAN', 'JOUB',
            'JULE', 'KIRB', 'KIRT', 'KUNO', 'KUZI', 'LAUF', 'LLAN', 'LONG', 'LOVI', 'LSAY', 'MACK',
            'MADI', 'MAND', 'MART', 'MAWS', 'MBIS', 'MEDL', 'MICH', 'MIZU', 'MYAL', 'NMED', 'NORF',
            'NVEG', 'ODBE', 'OLDH', 'OMGA', 'ONGU', 'PATE', 'PAUL', 'PCHA', 'PENG', 'PETE', 'PGEO',
            'PIGE', 'PISL', 'PMAR', 'POSS', 'POWE', 'RAUE', 'RNVG', 'ROOK', 'RUMP', 'SAXU', 'SCUL',
            'SHEI', 'SHLY', 'SIGA', 'STAN', 'STEN', 'SVIS', 'TAYH', 'TRYN', 'TURR', 'VESN', 'VESS',
            'WATT', 'WAYA', 'WEDD', 'WIDE', 'WINK', 'WPEC', 'YALO', 'YTRE']

#dataframe=pd.DataFrame(columns=['ImageName1','ImageName2','SIZE1','SIZE2','X1','Y1','X2','Y2'])
data_path = args.path
for image in os.listdir(data_path):
    print (image)
    for colony in range(1, len(colonies)):
        if image.startswith('['+colonies[colony]+']'):
            print ('found Source GEOTIFF Images '+ data_path+image)
            img1=cv2.imread(data_path+image)
            for image2 in os.listdir(data_path):
                if image2.startswith('['+colonies[colony]+']'):
                    img2 = cv2.imread(data_path+image2)
                    #size1 = int(math.ceil(os.path.getsize(data_path+image)/(1024*1024)))
                    #size2 = int(math.ceil(os.path.getsize(data_path+image2)/(1024*1024)))
                    print ('found Target GEOTIFF Images '+ data_path+image2)
                    tmp_dict = {}
                    tmp_dict["img1"] = data_path+image
                    tmp_dict["img2"] = data_path+image2
                    tmp_dict["x1"] = img1.shape[0]
                    tmp_dict["y1"] = img1.shape[1]
                    tmp_dict["x2"] = img2.shape[0]
                    tmp_dict["y2"] = img2.shape[1]
                    data.append(tmp_dict)
#json_dict["filename"] = filename
json_dict["Dataset"] = data

with open("images.json", "w") as outfile:
    json.dump(json_dict, outfile, indent=4, sort_keys=True)
