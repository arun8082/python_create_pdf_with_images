import paginate as paginate
from flask import Flask, render_template, request, redirect, session, url_for, Blueprint
from flask_paginate import Pagination, get_page_parameter, get_page_args
import base64
import json
import support_functions as sf

app = Flask(__name__, template_folder='template')
app.secret_key = "eci data"
mod = Blueprint('data', __name__)

@app.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@app.route("/login")
def login_page():
    return redirect("/")


@app.route("/login", methods=["POST"])
def loginProcess():
    fromdata = request.form
    username = fromdata["username"]
    password = fromdata["password"]
    status = sf.verify_user_credential(username, password)
    if status == False:
        error = "Invalid login credentials"
        return render_template("login.html", errors=error)
    else:
        session["username"] = username
        return redirect("choose_assembly")


@app.route("/view_report")
def view_report():
    try:
        username = session["username"]
        choosed_assembly = session["assembly"]
        type=session["type"]
    except KeyError:
        error = "Unauthorized access. Try to login"
        return redirect(url_for("login", errors=error))
    
    if username != None and username != "":
        
        page, per_page, offset = get_page_args(page_parameter='page',per_page_parameter='per_page')
        data = sf.get_pagination_data(choosed_assembly,type,offset=offset, per_page=per_page)
        pagination_data = data[0]
        total = data[1]
        pagination = Pagination(page=page, total=len(sf.report_data(choosed_assembly,type)),record_name='data',per_page_parameter="per_page",css_framework='bootstrap4')
        return render_template("myreport.html",data=pagination_data,page=page,
        per_page=per_page,pagination=pagination,type=type,assembly=choosed_assembly)
        

@app.route("/choose_assembly", methods=["GET"])
def choose_assembly_get():
    try:
        username = session["username"]
    except KeyError as k:
        # print("get", k)
        error = "Unauthorized access. Try to login"
        return redirect(url_for("login", errors=error))
    return render_template("choose_assembly.html")


@app.route("/choose_assembly", methods=["POST"])
def choose_assembly():
    try:
        username = session["username"]
        choosed_assembly = request.form["assembly"]
        if len(choosed_assembly) and len(choosed_assembly) != 0 and choosed_assembly != "":
            session["assembly"] = choosed_assembly
            session["type"]=request.form["type"]
        else:
            error="Please select any assembly"
            return render_template("choose_assembly.html",errors=error)
    except KeyError as k:
        error = "Unauthorized access. Try to login"
        return redirect(url_for("login", errors=error))
    return redirect("view_report")


@app.route("/logout")
def logout():
    session.clear()
    success = "Logout successfully."
    return redirect(url_for("login", success=success))

if __name__ == "__main__":
    app.run(debug=True,port=443,ssl_context='adhoc',host="10.10.48.10")