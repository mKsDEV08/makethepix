import sys
sys.path.append("../")

from flask import Flask, redirect, render_template, session, request, flash
from connector import User, db
from flask_session import Session

from werkzeug.security import generate_password_hash, check_password_hash

from helpers import login_required, user_exist, generate_id

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
@login_required
def index():
    return render_template("dashboard.html")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect("/")

        return render_template("register.html")
    
    elif request.method == "POST":

        form_username = request.form.get("username")
        form_pix = request.form.get("pix_key")
        form_password = request.form.get("password")

        if user_exist(User.username, form_username):
            flash("Usuário já existe!")
            return redirect("/register")
        
        new_user = User(form_username, generate_password_hash(form_password), generate_id(), 0.0, form_pix, 1.35)
        db.add(new_user)
        db.commit()

        user_id = db.query(User.uid).filter(User.username == form_username)
        user_id = user_id[0][0]

        session["user_id"] = user_id
        return redirect("/")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "GET":
        if session.get("user_id"):
            return redirect("/")

        return render_template("login.html")
    
    elif request.method == "POST":

        form_username = request.form.get("username")
        form_password = request.form.get("password")

        if not user_exist(User.username, form_username):
            flash("Usuário inexistente!")
            return redirect("/login")

        user_in_db = db.query(User.password_hash, User.uid, User.username).filter(User.username == form_username)
        user_in_db = user_in_db[0]
        
        if not check_password_hash(user_in_db[0], form_password):
            flash("Senha incorreta!")
            return redirect("/login")
        
        session["user_id"] = user_in_db[1]
        return redirect("/")


@app.route('/logout', methods=['GET'])
def logout():
    session["user_id"] = None
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)