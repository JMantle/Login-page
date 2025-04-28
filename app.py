from flask import Flask, render_template, redirect, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

app = Flask(__name__)
app.secret_key = ""   ## ENTER SECRET KEY HERE

def get_db_connection():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/loginSubmit", methods=["POST"])
def inputSubmitted():
    username = request.form["username"]
    attemptedPassword = request.form["password"]
    conn = get_db_connection()
    found = conn.execute("SELECT password FROM logins WHERE username = ?", (username,)).fetchone()
    conn.close()
    if found:
        if check_password_hash(found[0], attemptedPassword):
            return render_template("/profile.html", username = username)
        else:
            flash("wrong password")
    else:
        flash("no accounts with this username")
    return redirect("/")

@app.route("/goToSignUp")
def goToSignUp():
    return render_template("signUpPage.html")

@app.route("/signUpSubmit", methods=["POST"])
def signUp():
    username = request.form["username"]
    hashedPassword = generate_password_hash(request.form["password"])
    conn = get_db_connection()
    found = conn.execute("SELECT password FROM logins WHERE username = ?", (username,)).fetchone()
    if found:
       conn.close()
       flash("Username already taken")
       return redirect("/signUpPage")
    else:
        conn.execute("INSERT INTO logins (username, password) VALUES (?, ?)", (username, hashedPassword)) 
        conn.commit()
        conn.close()
        return redirect("/")
    
@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
    