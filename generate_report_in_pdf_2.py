from flask import Flask, render_template
import base64
import os

fold = 'S22_AC_27'
duplicate_dir  = f'static/{fold}/S_22/duplicate_images/'
#suspense_dir = f'../{fold}/suspense/'
#csv_path = f'../{fold}/report.c'

index_folds = []
index_folds.extend(os.listdir(duplicate_dir))
#index_folds.extend(os.listdir(suspense_dir))

max_dup_len = 0
index_folds.sort()
final_list = []
for ref in index_folds:
    
    ref_short = ref[:]
    ref_full_path = os.path.join( duplicate_dir, ref )
    
    
    dup = []
    if os.path.exists( ref_full_path ):
        files = os.listdir(ref_full_path)
        for f in files:
            
            if f[:3]=='REF':
                dup.append((ref_short, f'{ref_full_path}/{f}'))
                continue
            elif f == "Thumbs.db":
                continue
            
            if not os.path.isdir(os.path.join(duplicate_dir, ref, f)):
                dup.append((f.split('.')[0], f'{ref_full_path}/{f}'))
        if len(dup)>max_dup_len:
            max_dup_len = len(dup)

    final_list.append(dup)

# print(final_list[:1])


#[ [(image1,image1base64), imag2, ..], [img1, img2]]

app = Flask(__name__,template_folder='template')

@app.route("/")
def show_tables():
    return render_template('myreport.html', data=final_list,max_length=max_dup_len)

if __name__ == "__main__":
    app.run(debug=True)
