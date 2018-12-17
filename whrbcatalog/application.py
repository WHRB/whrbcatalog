# pylint: disable=C0103
"""
WHRB Chekhov
CS50 Final Project: Chris Sun, Joyce Lu, Simon Eder
"""

from tempfile import mkdtemp
from cs50 import SQL
from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 test to use SQLite database
db = SQL("sqlite:///chekhov.db")


@app.route("/homepage")
def homepage():
    """Render homepage"""
    return render_template("homepage.html")


@app.route("/", methods=["GET", "POST"])
def search():
    """Show a search page"""
    if request.method == "POST":

        # Grab the type of search the user is requesting
        searchtype = request.form.get("searchtype")

        # Create an allcaps list of all the words the user has inputted
        qlist = request.form.get("query").upper().split()

        # Create search parameters for the url
        search_params = searchtype + "@" + "*".join(qlist)

        # Redirect to index with search parameters
        return redirect(url_for('index', search=search_params, page=1))

    return render_template("search.html")


@app.route("/index")
def index():
    """Show a table"""
    # Request the page argument from the url
    page = request.args.get('page', default=1, type=int)

    # Request the search argument from the url
    presearch = request.args.get('search', default=None, type=None)

    # If no search argument (eg: going directly to index from the link or url)
    if presearch is None:
        # Pull 100 rows from the library, offset based on the page url parameter
        rows = db.execute(
            "SELECT * FROM library ORDER BY period, composer LIMIT 100 OFFSET :offset",
            offset=page*50 - 50
        )

        # NOTE: rowcount was too unwieldy in SQLite so we ended up commenting out these parts in the python and html!
        # rowcountlist = db.execute("SELECT count(*) FROM library")
        # rowcountdict = rowcountlist[0]
        # rowcount = rowcountdict.get("count(*)")

        # Render index page
        return render_template("index.html", rows=rows, rowcount=len(rows))

    # If search parameters exist (eg: going from the search form)
    # Separate the searchtype from the query
    search_params = presearch.split("@")

    # Store the searchtype
    searchtype = search_params[0]

    # Create a list of search keywords from the query
    qlist = search_params[1].split("*")

    # Add % signs to both sides of each searchword so that SQL LIKE will search all instances
    query = ["%" + item + "%" for item in qlist]

    # If the user searchs by everything
    if searchtype == "Everything":
        # Add quotes around the first searchword
        firstquery = "'" + query[0] + "'"

        # Create an empty list
        sql = []

        # Create a SQL query systematically across a list
        sql.append("SELECT * FROM library WHERE UPPER(period) LIKE " + firstquery)
        sql.append(" OR UPPER(composer) LIKE " + firstquery)
        sql.append(" OR UPPER(title) LIKE " + firstquery)
        sql.append(" OR UPPER(artist) LIKE " + firstquery)
        sql.append(" OR UPPER(label) LIKE " + firstquery)
        sql.append(" OR UPPER(length) LIKE " + firstquery)
        sql.append(" OR UPPER(format) LIKE " + firstquery)

        # If there is more than one searchword iterate across each one
        for item in query[1:]:

            # Put quotes around the searchword
            quoteitem = "'" + item + "'"

            # Add onto the SQL Query
            sql.append(" INTERSECT SELECT * FROM library WHERE UPPER(period) LIKE " + quoteitem)
            sql.append(" OR UPPER(composer) LIKE " + quoteitem)
            sql.append(" OR UPPER(title) LIKE " + quoteitem)
            sql.append(" OR UPPER(artist) LIKE " + quoteitem)
            sql.append(" OR UPPER(label) LIKE " + quoteitem)
            sql.append(" OR UPPER(length) LIKE " + quoteitem)
            sql.append(" OR UPPER(format) LIKE " + quoteitem)

        # Order by period, then composer so that new entries to the database will still be ordered,
        # offset based on page param
        sql.append("ORDER BY period, composer LIMIT 100 OFFSET " + str(page * 50 - 50))

        # Join the list together and run it as a SQL query
        rows = db.execute("".join(sql))

        # Render index
        return render_template("index.html", rows=rows)

    # If the user searches by a specific category
    # Create an empty list
    sql = []

    # Create a SQL search query
    sql.append("SELECT * FROM library ")
    sql.append("WHERE UPPER(" + searchtype.lower() + ") LIKE ")
    sql.append("'" + query[0] + "'")

    # Iterate over additional keywords
    for item in query[1:]:
        sql.append(" OR UPPER(" + searchtype.lower() + ") LIKE ")
        sql.append("'" + item + "'")

    # Order the search query
    sql.append("ORDER BY period, composer LIMIT 100 OFFSET " + str(page * 50 - 50))

    # Join the list together and run it as a SQL query
    rows = db.execute("".join(sql))

    # Render index
    return render_template("index.html", rows=rows)


@app.route("/flag", methods=["GET", "POST"])
def flag():
    """Flag a missing or damaged record"""

    # If the user submits a flag request
    if request.method == "POST":
        # Grab the existing notes for the track
        oldnote = db.execute("SELECT notes FROM library WHERE id=:trackid",
                             trackid=request.form.get("trackid"))

        # If there are no existing notes update without a line break
        if oldnote[0]['notes'] == "":
            db.execute("UPDATE library SET notes = :newnote, flagged=1 WHERE id=:trackid",
                       newnote=request.form.get("problem"), trackid=request.form.get("trackid"))
            return redirect("/")

        # If there are existing notes update with a line break
        note = oldnote[0]['notes'] + ";\n" + request.form.get("problem")

        db.execute("UPDATE library SET notes = :newnote, flagged=:flagged WHERE id=:trackid",
                   newnote=note, flagged=1, trackid=request.form.get("trackid"))
        return redirect("/")

    return render_template("flag.html")


@app.route("/addrecord", methods=["GET", "POST"])
@login_required
def addrecord():
    """Add a record to the database"""
    if request.method == "POST":
        # Take the user's form input and insert it into the library database
        db.execute(("INSERT INTO library (period, composer, title, artist, label, format, number, length, notes)"
                    " VALUES (:period, :composer, :title, :artist, :label, :format, :number, :length, :notes)"),
                   period=request.form.get("period"), composer=request.form.get("composer"),
                   title=request.form.get("title"), artist=request.form.get("artist"),
                   label=request.form.get("label"), format=request.form.get("format"),
                   number=request.form.get("number"), length=request.form.get("length"),
                   notes=request.form.get("notes"))
        return render_template("addrecord.html")

    return render_template("addrecord.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""

    # Store the user's requested username
    new_username = request.args.get('username')

    # Query the users table for the new username
    rows = db.execute("SELECT * FROM users WHERE username = :username",
                      username=new_username)

    # If the new username is blank or already exists, return a JSON false
    if not new_username or rows:
        return jsonify(False)

    # Otherwise return a JSON true
    return jsonify(True)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)

        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # If there is already a match for the username, return an apology
        if rows:
            return render_template("register.html")

        # If the password doesn't match the confimation password, return an apology
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("password and confirmation don't match", 400)

        # Create a hash for the user's password
        newhash = generate_password_hash(request.form.get("password"), method='pbkdf2:sha256', salt_length=8)

        # Add the new user and their hashed password to database table users
        db.execute("INSERT INTO users (username, hash) VALUES (:username, :newhash)",
                   username=request.form.get("username"), newhash=newhash)

        # Find the unique id number of the new user
        rows = db.execute("SELECT id FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Store the user's id for the duration of the login session
        session["user_id"] = rows[0]["id"]

        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
