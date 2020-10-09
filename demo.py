from flask import Flask, render_template
import base64

app = Flask(__name__,template_folder='template')

@app.route("/")
def show_tables():
    with open(r"static\343524\images\15887717869236588_base64_0343524.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
    #print(encoded_string)
    data=[[("name1",encoded_string),
          ("name2", encoded_string)],
          [("name3", encoded_string),
          ("name4", encoded_string)],
          [("name5", encoded_string),
          ("name6", encoded_string)]
          ]
    return render_template('myreport.html', data=data,max_lengh=10,
                           titles=['na', 'Female surfers', 'Male surfers'])

if __name__ == "__main__":
    app.run(debug=True)
