import os
from bson.objectid import ObjectId
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'mytestdb'
app.config["MONGO_URI"] = os.getenv('MONGO_URI','mongodb://root:Flash23@ds119072.mlab.com:19072/mytestdb')


mongo = PyMongo(app)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html", schoolforms=mongo.db.forms_db.find())
    
@app.route('/add_form')
def add_form():
    return render_template('addform.html')
    
@app.route('/insert_form', methods=['POST'])
def insert_form():
    schoolforms =  mongo.db.forms_db
    schoolforms.insert_one(request.form.to_dict())
    return redirect(url_for('index'))
    
@app.route('/edit_form/<form_id>')
def edit_form(form_id):
    schoolform =  mongo.db.forms_db.find_one({"_id": ObjectId(form_id)})
    return render_template('editform.html', schoolform=schoolform)
    
@app.route('/update_form/<form_id>', methods=["POST"])
def update_form(form_id):
    mongo.db.forms_db.update(
        {'_id': ObjectId(form_id)},
        {
            'Form': request.form.get('Form'),
            'Teacher': request.form.get('Teacher')
        })
    return redirect(url_for('index'))
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)