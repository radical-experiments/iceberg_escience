import pandas as pd
import sys

if __name__ == "__main__":

    images = pd.read_csv('Des3Images.csv')

    nodes = int(sys.argv[1])

    node_dists = list()
    for i in range(nodes):
        df = pd.DataFrame(columns=['ImageName1','ImageName2','SIZE1','SIZE2','X1','Y1','X2','Y2'])
        node_dists.append(df)

    images.sort_values(['SIZE1']+['SIZE2'])
    images.reset_index(drop='index',inplace=True)

    for idx, row in images.iterrows():
        node_idx = idx % nodes
        node_dists[node_idx].loc[len(node_dists[node_idx])] = [row['ImageName1'],row['ImageName2'],row['SIZE1'],row['SIZE2'],row['X1'],row['Y1'],row['X2'],row['Y2']]

    for i in range(nodes):
        node_dists[node_idx].to_csv('node%i_images.csv' % i,index=False)

