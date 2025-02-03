from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
utc_now = datetime.now(pytz.utc)
ist_time = utc_now.astimezone(pytz.timezone('Asia/Kolkata'))

class ToDo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=ist_time)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method == "POST":
        
        title = str(request.form.get('title'))
        desc = str(request.form.get('desc'))
        todo=ToDo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = ToDo.query.all()
    return render_template("index.html", alltodo=alltodo)

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    todo = ToDo.query.filter_by(sno=sno).first()

    if request.method == "POST":
        title = request.form.get('title')
        desc = request.form.get('desc')
        todo = ToDo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc     
        db.session.add(todo)        
        db.session.commit()
        return redirect("/")
    return render_template("update.html", todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = ToDo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route("/about/")
def about():
    
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True, port=5000)