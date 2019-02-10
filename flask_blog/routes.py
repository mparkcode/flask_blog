from flask import render_template, request, redirect, url_for
from flask_blog import app, mongo
from bson.objectid import ObjectId
from flask_uploads import UploadSet, configure_uploads, IMAGES


photos = UploadSet('photos', IMAGES)

app.config['UPLOADED_PHOTOS_DEST'] = 'flask_blog/static/img'
configure_uploads(app, photos)

@app.route("/")
def index():
    sessions = mongo.db.study_session.find()
    return render_template('index.html', sessions = sessions)

@app.route("/view_all")
def view_all():
    sessions = mongo.db.study_session.find()
    return render_template('view_all.html', sessions = sessions)

def save_picture_to_s3(form_picture):          
    random_hex = ''.join([random.choice(string.digits) for n in range(8)])    
    _, f_ext = os.path.splitext(form_picture.filename)  
    picture_fn = random_hex + f_ext
    s3 = boto3.resource('s3')
    s3.Bucket('mpark-flask-training-calendar').put_object(Key="static/workout_pics/" + picture_fn, Body=form_picture)
    return picture_fn 

@app.route("/add_a_session", methods=["POST", "GET"])
def add_a_session():
    form_values = request.form.to_dict()
    if request.method == "POST":
        for photo in request.files:
            filename = "img/" + photos.save(request.files[photo])
            for k,v in form_values.items():
                if k.startswith(photo):
                    form_values[k]=filename
                    nk = k.split().pop()
                    " ".join(nk)
                    form_values[nk] = form_values.pop(k)
        print(form_values)
        # mongo.db.study_session.insert_one(form_values)
        return "post route"
    else:
        return render_template("add_a_session.html")

@app.route("/view_detail/<session_id>")
def view_detail(session_id):
    session = mongo.db.study_session.find_one({"_id": ObjectId(session_id)})
    print(session)
    return render_template("view_detail.html", session=session)