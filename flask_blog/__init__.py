from flask import Flask
import os
from flask_pymongo import PyMongo
from flask_s3 import FlaskS3


app = Flask(__name__)
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.config["FLASKS3_BUCKET_NAME"] = os.environ.get("AWS_STORAGE_BUCKET_NAME")
mongo = PyMongo(app)
s3 = FlaskS3(app)

from flask_blog import routes