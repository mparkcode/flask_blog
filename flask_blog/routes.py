from flask import render_template, request, redirect, url_for
from flask_blog import app, mongo
from bson.objectid import ObjectId


@app.route("/")
def index():
    sessions = mongo.db.study_session.find()
    return render_template('index.html', sessions = sessions)

@app.route("/view_all")
def view_all():
    sessions = mongo.db.study_session.find()
    return render_template('view_all.html', sessions = sessions)

@app.route("/add_a_session", methods=["POST", "GET"])
def add_a_session():
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db.study_session.insert_one(form_values)
        print(form_values)
        return "Post route"
    else:
        return render_template("add_a_session.html")

@app.route("/view_detail/<session_id>")
def view_detail(session_id):
    session = mongo.db.study_session.find_one({"_id": ObjectId(session_id)})
    return render_template("view_detail.html", session=session)