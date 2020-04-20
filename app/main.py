from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os
  
def getApp():
    return app

app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

####### Database####### 
## app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/somil/Desktop/todo/todo.db
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/alantyping/workspace/flask_personal/alanweb/app/todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'todo.db')
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db')
  
db = SQLAlchemy(app) 
  
class Todo(db.Model): 
    id = db.Column(db.Integer, primary_key = True) 
    text = db.Column(db.String(200)) 
    complete = db.Column(db.Boolean) 
  
###### Route when nothing is specified in the url######  
@app.route('/todo') 
def todo(): 
    incomplete = Todo.query.filter_by(complete = False).all() 
    complete = Todo.query.filter_by(complete = True).all() 
  
    return render_template('todo.html', incomplete = incomplete, complete = complete) 
  
###### Adding items###### 
@app.route('/add', methods =['POST']) 
def add(): 
    todo = Todo(text = request.form['todoitem'], complete = False) 
    db.session.add(todo) 
    db.session.commit() 

###### Makes to stay on the same home page######  
    return redirect(url_for('todo')) 

###### Delete item###### 
@app.route('/delete/<id>') 
def delete(id): 
    Todo.query.filter(Todo.id == id).delete()
    db.session.commit() 
  
###### Makes to stay on the same home page######  
    return redirect(url_for('todo')) 
  
###### Complete items###### 
@app.route('/complete/<id>') 
def complete(id): 
  
    todo = Todo.query.filter_by(id = int(id)).first() 
    todo.complete = True
    db.session.commit() 
    ###### Makes to stay on the same home page######  
  
    return redirect(url_for('todo')) 
  
@app.route('/projects/')
def projects():
    return render_template("projects.html")

@app.route('/resume/')
def resume():
    return render_template("resume.html")

@app.route('/about/')
def about():
    return render_template("about.html")

# # if __name__=="__main__":
#     app.run(debug=True)