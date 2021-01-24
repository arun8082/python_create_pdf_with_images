'''
Program creates
'''

import pandas as pd 
import os


data_dir = '../data/'
const = 'S05_AC_25'  
type = 'duplicate_images'

folds_list = os.listdir(os.path.join(data_dir, const, f'S_{const[1:3]}', type))
folds_list.sort()
folds_count = len(folds_list)
cluster_ids = [i for i in range(1, folds_count+1)]

df = pd.DataFrame({'cluster_id':cluster_ids, "folder_names":folds_list})
# print(df.head)
df.to_csv(f'data/{const}_{type}_clusterID_mapping.csv', index=False)