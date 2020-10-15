import json
import base64
import os

def verify_user_credential(username,password):
    with open(r"private_data\users.json") as f:
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
    data=gererate_report_data(basepath,type)
    print("len(data)=>",len(data))
    return data

def get_pagination_data(choosed_assembly,type,offset=0, per_page=10):
    data = report_data(choosed_assembly,type)
    return data[offset: offset + per_page],len(data)

def gererate_report_data(choosed_assembly,type):
    duplicate_dir  = f'{choosed_assembly}/{type}/'
    print("duplicate_dir",duplicate_dir)
    index_folds = []
    index_folds.extend(os.listdir(duplicate_dir))
    # print("index_folds=>",len(index_folds))
    max_dup_len = 0
    index_folds.sort()
    final_list = []
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