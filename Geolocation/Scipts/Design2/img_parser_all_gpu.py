import json
import os
import csv
import argparse
import collections
import numpy as np
import cv2
import pandas as pd
import math

parser = argparse.ArgumentParser()

parser.add_argument('source_img',help='Path of the Target dataset')
parser.add_argument('path', help='Path of the Target dataset')
args = parser.parse_args()


dataframe=pd.DataFrame(columns=['ImageName1','ImageName2','SIZE1','SIZE2','X1','Y1','X2','Y2'])
src_path = args.source_img
trg_path = args.path
print src_path
print trg_path
for path, dirs,src_images in os.walk(src_path):
    for img in src_images :
        if img.startswith("RGB") and img.endswith(".tif"):
            img1=cv2.imread(src_path+'/'+img)
            print ('found Source GEOTIFF Images '+src_path+'/'+img)
            for path, dirs, files in os.walk(trg_path):
                for filename in files:
                    if filename.startswith("RGB") and filename.endswith(".tif"):
                        #img1=cv2.imread(args.source_img+img)   
                        img2 = cv2.imread(trg_path+'/'+filename)
			size1 = int(math.ceil(os.path.getsize(src_path+img)/(1024*1024)))
			size2 = int(math.ceil(os.path.getsize(trg_path+filename)/(1024*1024)))
                        print ('found Target GEOTIFF Images '+trg_path+'/'+filename)
			try:
                                  session_data = {
                                                        'ImageName1'      : src_path+img,
                                                        'ImageName2'      : trg_path+filename,
                                                        'SIZE1'           : size1,
							'SIZE2'		  : size2,
                                                        'X1'	          : img1.shape[0],
							'Y1'		  : img1.shape[1],
							'X2'		  : img2.shape[0],
							'Y2'		  : img2.shape[1]
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

