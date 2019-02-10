from flask import Flask, render_template, request, redirect, url_for
import os
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

mongo = PyMongo(app)

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


if __name__ == "__main__":
    app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)