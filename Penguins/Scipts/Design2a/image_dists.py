import pandas as pd
import sys

if __name__ == "__main__":

    images = pd.read_csv('Des3Images.csv')

    nodes = int(sys.argv[1])

    node_dists = list()
    for i in range(nodes):
        df = pd.DataFrame(columns=['Filename','Size'])
        node_dists.append(df)

    images.sort_values('Size', axis=0,inplace=True)
    images.reset_index(drop='index',inplace=True)
    for idx, row in images.iterrows():
        node_idx = idx % nodes
        node_dists[node_idx].loc[len(node_dists[node_idx])] = [row['Filename'],row['Size']]

    for i in range(nodes):
        node_dists[node_idx].to_csv('node%i_images.csv' % i,index=False)

