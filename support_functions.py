import json
import base64
import os
import pandas as pd

def verify_user_credential(username,password):
    with open(r"private_data/users.json") as f:
        users_credentials=json.load(f)["users"]
    status = False
    for users_credential in users_credentials:
        if users_credential["username"] == username and users_credential["password"] == password:
            status = True
            break
    return status

def report_data(choosed_assembly,type):
    with open("private_data/assembly_wise_base_paths.json") as f:
        assembly_wise_data = json.load(f)["base_paths"]
    basepath = assembly_wise_data[choosed_assembly]
    if choosed_assembly == 'S05_AC_25':
        data = gererate_report_data_with_names(basepath,type)
        print("len(data)=>",len(data))
        return data

        
    data=gererate_report_data(basepath,type)
    print("len(data)=>",len(data))
    return data

def get_pagination_data(choosed_assembly,type,offset=0, per_page=10):
    data = report_data(choosed_assembly,type)
    # per_page = len(data)
    return data[offset: offset + per_page],len(data)

def gererate_report_data(choosed_assembly,type):
    duplicate_dir  = f'{choosed_assembly}/{type}/'
    print("duplicate_dir",duplicate_dir)
    index_folds = []
    final_list = []
    if not os.path.exists(duplicate_dir):
        return final_list
    index_folds.extend(os.listdir(duplicate_dir))
    # print("index_folds=>",len(index_folds))
    max_dup_len = 0
    index_folds.sort()
    for ref in index_folds:
        
        ref_short = ref[4:]
        ref_full_path = os.path.join( duplicate_dir, ref )
                
        dup = []
        if os.path.exists( ref_full_path ):
            files = os.listdir(ref_full_path)
            for f in files:
                # print('ref_full_path/f',f'{ref_full_path}/{f}')
                if f[:3]=='REF':
                    with open(f'{ref_full_path}/{f}', "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    dup.append((ref_short, encoded_string))
                    continue
                elif f == "Thumbs.db":
                    continue
                if not os.path.isdir(os.path.join(duplicate_dir, ref, f)):
                    with open(f'{ref_full_path}/{f}', "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    dup.append((f.split('.')[0], encoded_string))
            if len(dup)>max_dup_len:
                max_dup_len = len(dup)
        final_list.append(dup)
    return final_list

def gererate_report_data_with_names(choosed_assembly,type):
    
    duplicate_dir  = f'{choosed_assembly}/{type}/'
    name_csv_path = 'data/S05_AC25_data_with_names.csv'
    df = pd.read_csv(name_csv_path)
    df.set_index('AUTO_ID', inplace=True)
    with open("data/S05_AC_25_matching_status.json") as jsonfile:
        data=json.load(jsonfile)
        partial_matching=data["partial_matching"]
        complete_matching=data["complete_matching"]
    
    print("duplicate_dir",duplicate_dir)
    index_folds = []
    index_folds.extend(os.listdir(duplicate_dir))
    index_folds.sort()
    # print("index_folds=>",len(index_folds))
    max_dup_len = 0
    index_folds.sort()
    final_list = []
    for ref in index_folds:
        matching_status = None
        if type == "duplicate_images":
            # print(f'{index["cluster_id"]}=>part:{index["cluster_id"] in partial_matching}=>com:{index["cluster_id"] in complete_matching}')
            if ref in partial_matching:
                matching_status = "Partial Matched"
            elif ref in complete_matching:
                matching_status = "Matched"
            # print(f'{ref}=>{index["cluster_id"]}=>{matching_status}')

        ref_short = ref[4:]
        ref_full_path = os.path.join( duplicate_dir, ref )
                
        dup = []
        if os.path.exists( ref_full_path ):
            files = os.listdir(ref_full_path)
            for f in files:
                # print('ref_full_path/f',f'{ref_full_path}/{f}')
                if f[:3]=='REF':
                    with open(f'{ref_full_path}/{f}', "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                    auto_id = int(ref_short.split('.')[0].split('_')[-1])
                    person_details_series = df.loc[auto_id]
                    
                    
                    st_code = person_details_series[0]
                    sc_no = person_details_series[1]
                    part_no = person_details_series[2]
                    slniopart = person_details_series[3]
                    name =  f'{person_details_series[4]} {person_details_series[5]}'
                    age = f'{person_details_series[6]}'
                    gender = f'{person_details_series[7]}'
                    Father_name =f'{person_details_series[8]} {person_details_series[9]}'
                    relation = f'{person_details_series[10]}'

                    dup.append(((st_code,sc_no,part_no,slniopart,auto_id,name,age,gender,Father_name,relation,matching_status,ref), encoded_string))
                    continue
                elif f == "Thumbs.db":
                    continue
                if not os.path.isdir(os.path.join(duplicate_dir, ref, f)):
                    with open(f'{ref_full_path}/{f}', "rb") as image_file:
                        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
                        
                    auto_id = int(f.split('.')[0].split('_')[-1])
                    person_details_series = df.loc[auto_id]
                    # print(person_details_series)
                    st_code = person_details_series[0]
                    sc_no = person_details_series[1]
                    part_no = person_details_series[2]
                    slniopart = person_details_series[3]
                    name =  f'{person_details_series[4]} {person_details_series[5]}'
                    age = f'{person_details_series[6]}'
                    gender = f'{person_details_series[7]}'
                    Father_name =f'{person_details_series[8]} {person_details_series[9]}'
                    relation = f'{person_details_series[10]}'

                    dup.append(((st_code,sc_no,part_no,slniopart,auto_id,name,age,gender,Father_name,relation,matching_status,ref), encoded_string))
                    
            if len(dup)>max_dup_len:
                max_dup_len = len(dup)
        final_list.append(dup)
    return final_list