import os
import shutil
import pandas as pd
import json
import sys

index=0
basepath = r"/home/dgs/prod_env/eci/data/S05_AC_25/S_05/"
subpath = ["duplicate_images","suspect"][index]
mapping_file = ["S05_AC_25_duplicate_images_clusterID_mapping.csv","S05_AC_25_suspect_clusterID_mapping.csv"][index]
action_file = ["S05_duplicate_images_action_sheet.csv","S05_suspect_action_sheet.csv"][index]

mapping_df = pd.read_csv(os.path.join("data",mapping_file))
mapping_df.set_index('cluster_id', inplace=True)

#move into replicates
with open(os.path.join("data","S05_AC_25_replicates.json")) as jsonfile:
    replicate_list = json.load(jsonfile)["cluster_id"]
if not os.path.exists(os.path.join(basepath,"delete")):
    os.makedirs(os.path.join(basepath,"delete"))
for i in range(len(replicate_list)):
    replicate_dirs = replicate_list[i]
    for j in range(len(replicate_dirs)-1):
        cluster_dir_path = mapping_df.loc[replicate_dirs[1]][0]
        for t in ["duplicate_images","suspect"]:
            if os.path.exists(os.path.join(basepath,t,cluster_dir_path)):
                src = os.path.join(basepath,t,cluster_dir_path)
                dest = os.path.join(basepath,"delete",cluster_dir_path)
                print(src,dest)
                shutil.move(src,dest)

sys.exit(0)


#move into siblings
with open(os.path.join("data","S05_AC25_siblings.json")) as jsonfile:
    siblings_list = json.load(jsonfile)["cluster_id"]

if not os.path.exists(os.path.join(basepath,"siblings")):
    os.makedirs(os.path.join(basepath,"siblings"))
for clstrId in siblings_list:
    try:
        cluster_dir_path = mapping_df.loc[clstrId][0]
        for t in ["duplicate_images","suspect"]:
            if os.path.exists(os.path.join(basepath,t,cluster_dir_path)):
                src = os.path.join(basepath,t,cluster_dir_path)
                dest = os.path.join(basepath,"siblings")
                # print(src,dest)
                shutil.move(src,dest)
    except Exception as e:
        print("ERROR:",e)

sys.exit(0)

# delete or move folders
action_df = pd.read_csv(os.path.join("data",action_file))
for i in range(len(action_df)):
    clstrId=action_df["CLUSTER ID"][i]

    cluster_dir_path = mapping_df.loc[clstrId][0]
    # print(cluster_dir_path)
    # print("cluster path ",mapping_df[clstrId])
    try:
        if action_df["REMARKS"][i].strip() == "move to suspect":
            src = os.path.join(basepath,subpath,cluster_dir_path)        
            dest = os.path.join(basepath,"suspect",cluster_dir_path)
            shutil.move(src,dest)
            print("INFO:","Suspect Move")
        elif action_df["REMARKS"][i].strip() == "move to duplicate":
            src = os.path.join(basepath,subpath,cluster_dir_path)        
            dest = os.path.join(basepath,"duplicate_images",cluster_dir_path)
            shutil.move(src,dest)
            print("INFO:","duplicate Move")
        elif action_df["REMARKS"][i].strip() == "delete":        
            src = os.path.join(basepath,subpath,cluster_dir_path)        
            if not os.path.exists:
                os.makedirs(os.path.join(basepath,"deteled"))
            dest = os.path.join(basepath,"deteled",cluster_dir_path)
            shutil.move(src,dest)
            print("INFO:","delete")
    except:
        pass
