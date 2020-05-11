import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database.db")




@app.route("/")
def index():
        return render_template('index.html')




@app.route("/index")
def home():
        return render_template('index.html')





# REGISTRAR USUÁRIO

@app.route("/registeruser", methods=["GET", "POST"])
def registeruser():
    session.clear()

    if request.method == "GET":
        return render_template('registeruser.html')
    else:
        username = request.form.get('username')
        if not username:
            return apology('Must provide a name')

        userpassword = request.form.get('userpassword')
        phash = generate_password_hash(userpassword)
        if not userpassword:
            return apology('Must provide a password')

        userconfirmation = request.form.get('userconfirmpassword')
        if userconfirmation != userpassword:
            return apology('Confirmation must be the same as the password')

        check = db.execute('SELECT username FROM users WHERE username = :username', username = username)
        if check:
            return apology('Username already in use')

        db.execute('INSERT INTO users (username, password) VALUES (:username, :hash)', username = username, hash = phash)

        rows1 = db.execute('SELECT * FROM users WHERE username = :username', username = username)

        session['user_id'] = rows1[0]['id']


        return redirect  ('userhome')



# REGISTRAR NGO

@app.route("/registerngo", methods=["GET", "POST"])
def registerngo():
    session.clear()

    if request.method == "GET":
        return render_template('registerngo.html')
    else:

        ngosname = request.form.get('ngosname')
        if not ngosname:
            return apology('Must provide a name')

        ngoswhatsapp = request.form.get('ngoswhatsapp')
        if not ngoswhatsapp:
            return apology('Must provide a Whatsapp')

        ngospassword = request.form.get('ngospassword')
        phash = generate_password_hash(ngospassword)
        if not ngospassword:
            return apology('Must provide a password')

        ngosconfirmation = request.form.get('ngosconfirmpassword')
        if ngospassword != ngosconfirmation:
            return apology('Confirmation must be the same as the password')

        check = db.execute('SELECT ngosname FROM ngos WHERE ngosname = :ngosname', ngosname = ngosname)
        if check:
            return apology('Name already in use')

        rows = db.execute('INSERT INTO ngos (ngosname, password, whatsapp) VALUES (:ngosname, :hash, :whatsapp)', ngosname = ngosname, hash = phash, whatsapp = ngoswhatsapp)

        rows1 = db.execute('SELECT * FROM ngos WHERE ngosname = :ngosname', ngosname = ngosname)

        session['user_id'] = rows1[0]['id']


        return redirect ('ngoshome')


# FAZER LOGIN

@app.route("/login")
def login():
    return render_template("login.html")



@app.route("/loginuser", methods=["GET", "POST"])
def loginuser():
    session.clear()

    if request.method == "POST":
        if not request.form.get("username"):
            return apology("Must provide a name")

        elif not request.form.get("password"):
            return apology("Must provide a password")

        rows = db.execute("SELECT * FROM users WHERE username = :username", username = request.form.get("username"))

        if len (rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("password")):
            return apology ("Invalid username or password")

        session["user_id"] = rows[0]["id"]


        return redirect("/userhome")

    else :
        return render_template("loginuser.html")


@app.route("/loginngo", methods=["GET", "POST"])
def loginngo():
    session.clear()

    if  request.method == "POST":
        if not request.form.get("ngosname"):
            return apology("Must provide a name")
        elif not request.form.get("ngospassword"):
            return apology("Must provide a password")

        rows = db.execute("SELECT * FROM ngos WHERE ngosname = :ngosname", ngosname = request.form.get("ngosname"))

        if len (rows) != 1 or not check_password_hash(rows[0]["password"], request.form.get("ngospassword")):
            return apology ("Invalid username or password")

        session["user_id"] = rows[0]["id"]


        return redirect("/ngoshome")

    else :
        return render_template("loginngo.html")



@app.route("/userhome")
def userhome():
    name = db.execute("SELECT username from users WHERE id = :id", id = session["user_id"])
    rows = db.execute("select * from cases")

    return render_template("userhome.html", name = name[0]['username'], rows = rows)





@app.route("/ngoshome")
def ngoshome():


    name = db.execute("SELECT ngosname FROM ngos WHERE id = :id", id = session["user_id"])
    rows = db.execute("SELECT * FROM cases WHERE casesid = :id", id = session["user_id"])

    return render_template("./ngoshome.html" , name = name[0]['ngosname'], rows = rows)


@app.route("/delete", methods=["GET", "POST"])
def delete():


    if request.method == "POST":
        id = request.form.get("id")
        db.execute("DELETE FROM cases WHERE id = :id", id = id)


    return redirect ('/ngoshome')



@app.route("/newcase", methods=["GET", "POST"])
def newcase():

    if request.method == "POST":

        if not request.form.get("casetitle"):
            return apology("Must provide a title")

        elif not request.form.get("casetext"):
            return apology("Must provide some text")

        elif not request.form.get("whatsapp"):
            return apology("Must provide whatsapp")



        db.execute("INSERT INTO cases (title, text, whatsapp, casesid) VALUES (:title, :text, :whatsapp, :casesid)", title = request.form.get("casetitle"), text = request.form.get("casetext"), whatsapp = request.form.get("whatsapp"), casesid = session["user_id"])


        return redirect ("./ngoshome")

    else :
        return render_template("./newcase.html")














































def apology(message):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=' ', bottom=escape(message))


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("index")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)