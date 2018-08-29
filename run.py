import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'mytestdb'
app.config["MONGO_URI"] = 'mongodb://root:Flash23@ds119072.mlab.com:19072/mytestdb'

mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", schoolforms=mongo.db.forms_db.find())
    
@app.route('/add_form')
def add_form():
    return render_template('addform.html',
    categories=mongo.db.categories.find())
    
@app.route('/insert_form', methods=['POST'])
def insert_form():
    schoolforms =  mongo.db.forms_db
    schoolforms.insert_one(request.form.to_dict())
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)