from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 
import uuid
import random
import string  
import secrets

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task.db"
# initialize the app with the extension
db.init_app(app)

# Create Your Tables
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(255), unique=False, nullable=True)
    importance = db.Column(db.String(255), unique=False, nullable=True)
    uuid = db.Column(db.String(255), unique=True, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now())

# Create the Tables
with app.app_context():
    db.create_all()

def generate_uuid5(name):
    current_datetime = datetime.now()
    secrets_str = ''.join(secrets.choice(string.ascii_letters + string.digits) for x in range(10))
    uuid_str = f"{name}_{secrets_str}_{current_datetime}"
    get_uuid5 = uuid.uuid5(uuid.NAMESPACE_DNS, uuid_str)
    return get_uuid5

@app.route("/hello_world")
def hello_world():
    html_var = "<p style='color:red;'>Hello, World!</p>"
    json_var = {"name":"Hello World"}
    return json_var

@app.route("/add/<int:a>/<int:b>")
def add(a,b):
    json_var = {"result":(a+b)}
    return json_var

@app.route("/", methods=['GET', 'POST'])
def index():
    context={}
    get_uuid = str(generate_uuid5("Task 1"))
    if request.method == 'POST':
        task = request.form['task']
        importance = request.form['importance']
        if task and importance :
            t = Task(task=task,importance=importance,uuid=get_uuid)
            db.session.add(t)
            db.session.commit()
            
    context['allTask'] = Task.query.all()
    return render_template('index.html',data=context)

@app.route("/delTask/<uid>/", methods=['GET', 'POST'])
def delTask(uid):
    getTask=Task.query.filter_by(uuid=uid).first()
    db.session.delete(getTask)
    db.session.commit()
    return redirect ("/")

@app.route("/updateTask/<uid>/", methods=['GET', 'POST'])
def updateTask(uid):
    context={}
    getTask = Task.query.filter_by(uuid=uid)
    taskName = [i.task for i in getTask][0]
    taskImp = [i.importance for i in getTask][0]
    context['allTask'] = Task.query.all()
    if request.method == 'POST':
        task = request.form['task']
        importance = request.form['importance']
        if task and importance : 
            getTask = Task.query.filter_by(uuid=uid).first()
            getTask.task = task
            getTask.importance = importance
            db.session.add(getTask)
            db.session.commit()
            return redirect ("/")
    return render_template('index.html',data=context,taskName=taskName,taskImp=taskImp)


if __name__== "__main__" :
    app.run(debug=True, port=5000)