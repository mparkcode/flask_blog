from flask import render_template, request, redirect, url_for, jsonify
from flask_blog import app, mongo
from bson.objectid import ObjectId
from flask_uploads import UploadSet, configure_uploads, IMAGES
import random
import string
import boto3
import os
import datetime

photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'flask_blog/static/img'
configure_uploads(app, photos)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/view_all")
def view_all():
    posts = mongo.db.posts.find()
    return render_template('view_all.html', posts = posts)

def save_picture_to_s3(form_picture):          
    random_hex = ''.join([random.choice(string.digits) for n in range(8)])    
    _, f_ext = os.path.splitext(form_picture.filename)  
    picture_fn = "img" + random_hex + f_ext
    s3 = boto3.resource('s3')
    s3.Bucket('flaskblog').put_object(Key="static/img/" + picture_fn, Body=form_picture)
    return picture_fn 

@app.route("/add_a_post", methods=["POST", "GET"])
def add_a_post():
    post={}
    post["1"] = {'date': {'date':datetime.date.today().strftime("%Y-%m-%d")}}
    p = mongo.db.posts.insert(post)
    return redirect(url_for('view_detail', post_id=p))

@app.route("/view_detail/<post_id>")
def view_detail(post_id):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    print(post_id)
    return render_template("view_detail.html", post=post, post_id=post_id)

@app.route("/<post_id>/add_note", methods=["POST", "GET"])
def add_note(post_id):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    print(post)
    if request.method == "POST":
        form_values = request.form.to_dict()
        mongo.db.posts.update(
            {'_id' : ObjectId(post_id)},
        {
            '$set': {str(len(post)) : {'note': form_values}}
        })
        return redirect(url_for('view_detail', post_id=post['_id']))
    return render_template("add_a_note.html", post=post)

@app.route("/<post_id>/add_picture", methods=["POST", "GET"])
def add_picture(post_id):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    if request.method == "POST":
        form_values = request.form.to_dict()
        print(form_values)
        print(request.files)
        for photo in request.files:
            print(photo)
            filename = save_picture_to_s3(request.files[photo])
            print(filename)
            for k,v in form_values.items():
                if k.startswith(photo):
                    form_values[k]=filename
                    nk = k.split().pop()
                    " ".join(k)
                    form_values[nk] = form_values.pop(k)
        print(form_values)
        
        mongo.db.posts.update(
            {'_id' : ObjectId(post_id)},
        {
            '$set': {str(len(post)) : {'picture': form_values}}
        })
        return redirect(url_for('view_detail', post_id=post['_id']))
    return render_template("add_a_picture.html", post=post)

@app.route("/delete/<post_id>/<key>", methods=["POST"])
def delete(post_id, key):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    print(post)
    del post[key]
    for i in range(1, len(post)):
        if str(i) in post.keys():
            print('yes')
        else:
            for j in range(i, len(post)):
                post[str(j)] = post.pop(str(j+1))
    print(post)
    mongo.db.posts.update({"_id": ObjectId(post_id)}, post)
    return redirect(url_for('view_detail', post_id=post['_id']))

@app.route("/add_note/<post_id>/<key>/<value>", methods=["POST"])
def add_ajax_note(post_id, key, value):
    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    print(post)
    post[str(len(post))] = {'note' :{key:value}}
    print(post)
    mongo.db.posts.update({"_id": ObjectId(post_id)}, post)
    return render_template("new_note.html", key=str(len(post)), a=key, b=value, post_id=post_id)

@app.route("/update_post/<post_id>", methods=["POST"])
def update_post(post_id):
    print(post_id)
    post = request.get_json()
    mongo.db.posts.update({"_id": ObjectId(post_id)}, post)
    return "Hi"
