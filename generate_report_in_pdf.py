from flask import Flask, render_template
import base64
import os

fold = 'S14_AC_48'
duplicate_dir  = f'../{fold}/duplicate_images/'
#suspense_dir = f'../{fold}/suspense/'
#csv_path = f'../{fold}/report.c'

index_folds = []
index_folds.extend(os.listdir(duplicate_dir))
#index_folds.extend(os.listdir(suspense_dir))

max_dup_len = 0
index_folds.sort()
final_list = []
for ref in index_folds[3700:]:
    
    ref_short = ref[4:]
    ref_full_path = os.path.join( duplicate_dir, ref )
    
    
    dup = []
    if os.path.exists( ref_full_path ):
        files = os.listdir(ref_full_path)
        for f in files:
            
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

# print(final_list[:1])


#[ [(image1,image1base64), imag2, ..], [img1, img2]]

app = Flask(__name__,template_folder='template')

@app.route("/")
def show_tables():
    # data=[("name1",encoded_string),
    #       ("name2", encoded_string),
    #       ("name3", encoded_string),
    #       ("name4", encoded_string),
    #       ("name5", encoded_string),
    #       ("name6", encoded_string)
    #       ]
    return render_template('myreport.html', data=final_list,max_length=max_dup_len)

if __name__ == "__main__":
    app.run(debug=True)
