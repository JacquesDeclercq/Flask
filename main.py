from flask import Flask, render_template, url_for, redirect, request, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, update, delete, values
from typing import Callable
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "BeCode"
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(minutes = 1)


#class MySQLAlchemy(SQLAlchemy):  # Or you can add the below code on the SQLAlchemy directly if you think to modify the package code is acceptable.
#    Column: Callable  # Use the typing to tell the IDE what the type is.
#    String: Callable
#    Integer: Callable

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key = True)  #("id" to give name, db.Integer, primary_key = True)
    name = db.Column( db.String(100))
    email = db.Column(db.String(100))

    def __init__(self,name, email):
        self.name = name
        self.email = email

#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' ## /// is a relative path, //// absolute path
#db = SQLAlchemy(app)


#class todo(db.Model):
#    id = db.Column(db.Integer, primary_key = True)
#    content = db.Column(db.String(200), nullable = False) ## makes sure the entry is not empty
#    date_created = db.Column(db.DateTime, default = datetime.utcnow)

#    def __repr__(self):
#        return '<Task %r>' % self.id

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/login', methods =['POST', 'GET'])
def login():
    if request.method == 'POST':
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        found_user = Users.query.filter_by(name = user).first()
        if found_user:
            session["email"] = found_user.email
        else:
            usr = Users(user, "")
            db.session.add(usr)
            db.session.commit() #you commit to save you can rollback to previous state

        flash("Login Succesful!", "info")
        return redirect(url_for("user"))
    else :
        if "user" in session:
            flash("Already logged in!", "info")
            return redirect(url_for("user"))

        return render_template("login.html")

@app.route("/user", methods = ["POST", "GET"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            found_user = Users.query.filter_by(name = user ).first()
            found_user.email = email
            db.session.commit()
            flash("Email was saved", "info")
        else :
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else :
        flash("You are not logged in!", "info")
        return redirect(url_for("login"))

@app.route("/view")
def view():
    return render_template("view.html", values = Users.query.all())

@app.route("/logout")
def logout():
    if "user" in session:
        user = session["user"]
        flash(f"You have been logged out {user}", "info") #warning, info and error
        session.pop("user", None)
        session.pop("email", None)
    return redirect(url_for("login"))

@app.route('/<name>')
def welcoming(name):
    return f"<h1>Hello {name}!</h1>"

@app.route("/<int:user_id>/delete", methods = ['POST', 'GET'])
def delete(user_id):
        if "user" in session:
            found_user = Users.query.get(user_id)
            db.session.delete(found_user)
            flash("You have been deleted", "info")
            db.session.commit()

        return redirect(url_for(("login")))

@app.route('/admin')
def admin():
    return redirect(url_for("welcoming", name = "Admin!")) ## no / to redirect to a function

@app.route('/calculate', methods = ['POST','GET'])
def calcul():
#    if request.method == 'POST':
#        data = request.json
#        if type(data['salary']) != int or type(data['bonus']) != int or type(data['taxes']) != int:
#            output = jsonify({'error': 'expected numbers, got strings.'})
#            return output
#        else:
#            result = data['salary'] + data['bonus'] - data['taxes']
#            output = jsonify({'result': result})
#            return output

    #salary = int(request.form["salary"])
    #bonus = int(request.form["bonus"])
    #taxes = int(request.form["taxes"])
    #user = salary + bonus - taxes
    #return redirect(url_for("user", usr = user ))

    return render_template("calculate.html")



if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
