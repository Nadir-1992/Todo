import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///Todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    Sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    des = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return f"{self.Sno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        title = request.form['title']
        des = request.form['des']
        todo = Todo(title=title, des=des)
        db.session.add(todo)
        db.session.commit()
    all_todo = Todo.query.all()
    return render_template("index.html", all_todo=all_todo)


@app.route("/update/<int:Sno>", methods=['GET', 'POST'])
def update(Sno):
    if request.method == 'POST':
        title = request.form['title']
        des = request.form['des']
        todo = Todo.query.filter_by(Sno=Sno).first()
        todo.title = title
        todo.des = des
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(Sno=Sno).first()
    return render_template("update.html", todo=todo)


@app.route("/delete/<int:Sno>")
def delete(Sno):
    todo = Todo.query.filter_by(Sno=Sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


# with app.app_context():
#     db.create_all()
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
