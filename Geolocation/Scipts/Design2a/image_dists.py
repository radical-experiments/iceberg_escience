import sys
import os
import numpy as np
from matplotlib import pyplot as plt
import pandas as pd

images = pd.read_csv('../Data/Geolocation_Image_pairs.csv')
nodes = 4
node_dists = list()
for i in range(nodes):
    df0 = pd.DataFrame(columns=['ImageName1','ImageName2','SIZE1','SIZE2','X1','Y1','X2','Y2'])
    df1 = pd.DataFrame(columns=['ImageName1','ImageName2','SIZE1','SIZE2','X1','Y1','X2','Y2'])
    df2 = pd.DataFrame(columns=['ImageName1','ImageName2','SIZE1','SIZE2','X1','Y1','X2','Y2'])
    df3 = pd.DataFrame(columns=['ImageName1','ImageName2','SIZE1','SIZE2','X1','Y1','X2','Y2'])
    
    node_dists.append(df)

images.sort_values(['SIZE1']+['SIZE2'])
images.reset_index(drop='index',inplace=True)

for idx, row in images.iterrows():
    node_idx = idx % nodes
    if node_idx == 0 :
        df0.loc[len(df0)] = [row['ImageName1'],row['ImageName2'],row['SIZE1'],row['SIZE2'],row['X1'],row['Y1'],row['X2'],row['Y2']]
        
    elif node_idx == 1:
        df1.loc[len(df1)] = [row['ImageName1'],row['ImageName2'],row['SIZE1'],row['SIZE2'],row['X1'],row['Y1'],row['X2'],row['Y2']]
        
    elif node_idx == 2:
        df2.loc[len(df2)] = [row['ImageName1'],row['ImageName2'],row['SIZE1'],row['SIZE2'],row['X1'],row['Y1'],row['X2'],row['Y2']]
        
    else:
        df3.loc[len(df3)] = [row['ImageName1'],row['ImageName2'],row['SIZE1'],row['SIZE2'],row['X1'],row['Y1'],row['X2'],row['Y2']]
    

df0.to_csv('/home/aymen/node1_images.csv' ,index=False)
df1.to_csv('/home/aymen/node2_images.csv' ,index=False)
df2.to_csv('/home/aymen/node3_images.csv' ,index=False)
df3.to_csv('/home/aymen/node4_images.csv' ,index=False)
