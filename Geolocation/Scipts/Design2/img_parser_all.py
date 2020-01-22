import json
import os
import csv
import math
import argparse
import collections
import numpy as np
import cv2
import pandas as pd 


parser = argparse.ArgumentParser()
parser.add_argument('source_img',help='Path of the Target dataset')
parser.add_argument('path', help='Path of the Target dataset')
args = parser.parse_args()
colonies = ['BEAU','BEDM','BRDN','BRDS','CROZ']
dataframe=pd.DataFrame(columns=['ImageName1','ImageName2','SIZE1','SIZE2','X1','Y1','X2','Y2'])
for colony in colonies:

        src_path = args.source_img+colony+'/Aerial/'
        trg_path = args.path+colony+'/Satellite/'
        print src_path
        print trg_path
        for path, dirs,src_images in os.walk(src_path):
            for img in src_images :
                if img.startswith("CA") and img.endswith(".tif"):
                   img1=cv2.imread(src_path+img)
                   print ('found Source GEOTIFF Images '+img)
                   for path, dirs, files in os.walk(trg_path):
                       for filename in files:
                           if filename.startswith("WV") and filename.endswith(".tif"):
                                #img1=cv2.imread(args.source_img+img)
				size1 = int(math.ceil(os.path.getsize(src_path+img)/(1024*1024)))
                        	size2 = int(math.ceil(os.path.getsize(trg_path+filename)/(1024*1024)))
                                img2 = cv2.imread(trg_path+filename)
                                print ('found Target GEOTIFF Images '+filename)
                                try:
                                        session_data = {
                                                                'ImageName1'      : src_path+img,
                                                                'ImageName2'      : trg_path+filename,
                                                                'SIZE1'           : size1,
                                                                'SIZE2'           : size2,
                                                                'X1'              : img1.shape[0],
                                                                'Y1'              : img1.shape[1],
                                                                'X2'              : img2.shape[0],
                                                                'Y2'              : img2.shape[1]
                                                        }
                                except Exception as e:
                                                        print e
                                                        session_data = {
                                                                'ImageName1'      : src_path+img,
                                                                'ImageName2'      : trg_path+filename,
                                                                'SIZE1'           : size1,
                                                                'SIZE2'           : size2,
                                                                'X1'              : img1.shape[0],
                                                                'Y1'              : img1.shape[1],
                                                                'X2'              : img2.shape[0],
                                                                'Y2'              : img2.shape[1]
                                                        }
                                                        pass


                                dataframe =  dataframe.append(session_data, ignore_index=True)
                                dataframe =  dataframe.reset_index().drop('index', axis=1)
                                dataframe.to_csv('Desc1CSV.csv',index=False)
