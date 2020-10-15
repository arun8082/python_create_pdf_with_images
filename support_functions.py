import json
import base64

def verify_user_credential(username,password):
    with open(r"private_data\users.json") as f:
        users_credentials=json.load(f)["users"]
    status = False
    for users_credential in users_credentials:
        if users_credential["username"] == username and users_credential["password"] == password:
            status = True
            break
    return status

def report_data(choosed_assembly):
    with open("private_data/assembly_wise_base_paths.json") as f:
        assembly_wise_data = json.load(f)["base_paths"]
    basepath = assembly_wise_data[choosed_assembly]

    with open(r"static\343524\images\15887717869236588_base64_0343524.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    #print(encoded_string)
    data=[[("name1",encoded_string),
          ("name2", encoded_string)],
          [("name3", encoded_string),
          ("name4", encoded_string)],
          [("name5", encoded_string),
          ("name6", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)],
          [("name1", encoded_string),
           ("name2", encoded_string)]
          ]
    return data

def get_pagination_data(choosed_assembly,offset=0, per_page=10):
    data = report_data(choosed_assembly)
    return data[offset: offset + per_page],len(data)
