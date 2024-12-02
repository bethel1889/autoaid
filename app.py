from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, check, C, M


# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///database/auto_aid.db")
LOCATIONS = db.execute("SELECT * FROM locations")

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# HOMEPAGE
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    id = session["user_id"]
    info = db.execute("SELECT * FROM users WHERE id=?;", id)[0]
    username = info["username"]
    role = info["role"]
    if role: role = "(Mechanic)"
    else: role = "(Customer)"
    return render_template("index.html", username=username, role=role)



# REGISTER
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("register.html")

    else:
        # Check if the username and password is valid
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        role = int(request.form.get("role"))

        if role not in [0, 1]: return apology("Select a role... are you a mechanic? or are you a customer?", 403)

        if check(username, password) == False: return apology("Enter username and password to login")

        # Check if the password and confirmation are both correct
        elif password != confirmation:
            return apology("Password and confirmation password do not match")

        # Check if the username exists in the database
        details = db.execute("SELECT * FROM users WHERE username=?;", username)
        if not details:
            # Enter the user's details into the database if the username doesn't exist
            db.execute("INSERT INTO users (username, hash, role) VALUES (?, ?, ?);",
                       username, generate_password_hash(password), role)
            rows = db.execute("SELECT * FROM users WHERE username=?;", username)

            # Log the user in
            session["user_id"] = rows[0]["id"]
            flash("You have been registered")
            return redirect("/")

        # if the username and password exist
        elif check_password_hash(details[0]["hash"], password) == True:
            return apology("You already have an account with MapleMatch")

        # If only the username exists
        else:
            return apology("Please choose a different username, this username has been taken")



# LOG IN
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""
    # Forget any user_id
    session.clear()

    if request.method == "GET":
        return render_template("login.html")
    else:
        # Ensure username was submitted
        if not request.form.get("username"): return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        flash("You have been logged in")
        return redirect("/")



# SEARCH FOR MECHANICS
@app.route("/mechanics", methods=["GET", "POST"])
@login_required
def mechanics():
    id = session["user_id"]
    info = db.execute("SELECT * FROM users WHERE id=?", id)[0]
    username = info["username"]
    role = info["role"]
    if role: role = "(Mechanic)"
    else: role = "(Customer)"

    if request.method == "GET":
        # Render mechanics search form
        return render_template("mechanics.html", username=username, role=role, LOCATIONS=LOCATIONS)
    else:
        # Search mechanics based on form input
        location_id = int(request.form.get("location"))
        if location_id:
            mechanics = db.execute('''SELECT
                users.id AS user_id,
                users.username AS username,
                profiles.display_name AS display_name,
                profiles.bio AS bio,
                profiles.email AS email,
                locations.name AS location_name
            FROM users
            JOIN profiles ON users.id = profiles.user_id
            JOIN locations ON profiles.location_id = locations.id
            WHERE locations.id=?;''', location_id)
        else:
            mechanics = db.execute('''SELECT
                users.id AS user_id,
                users.username AS username,
                profiles.display_name AS display_name,
                profiles.bio AS bio,
                profiles.email AS email,
                locations.name AS location_name
            FROM users
            JOIN profiles ON users.id = profiles.user_id
            JOIN locations ON profiles.location_id = locations.id;''')
        return render_template("mechanics.html", username=username, role=role, mechanics=mechanics, LOCATIONS=LOCATIONS)



# VIEW PROFILE
@app.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    id = session["user_id"]
    info = db.execute("SELECT * FROM users WHERE id=?", id)[0]
    username = info["username"]
    role = info["role"]
    if role: role = "(Mechanic)"
    else: role = "(Customer)"
    if request.method == "GET":
        # show the user their profile and issues
        issues = db.execute('''SELECT
            issues.id AS issue_id,
            issues.title AS issue_title,
            issues.body AS issue_body,
            issues.status AS issue_status,
            issues.user_id AS issue_user_id,
            users.username AS user_name,
            profiles.display_name AS profile_display_name,
            profiles.bio AS profile_bio,
            profiles.email AS profile_email,
            locations.name AS location_name,
            locations.id AS location_id
        FROM
            issues
        JOIN
            users ON issues.user_id = users.id
        JOIN
            profiles ON users.id = profiles.user_id
        JOIN
            locations ON profiles.location_id = locations.id
                            WHERE issues.user_id=?''', id)
        profile = db.execute('''SELECT
                users.id AS user_id,
                users.username AS username,
                profiles.display_name AS display_name,
                profiles.bio AS bio,
                profiles.email AS email,
                locations.name AS location_name
            FROM users
            JOIN profiles ON users.id = profiles.user_id
            JOIN locations ON profiles.location_id = locations.id
            WHERE users.id=?;''', id)
        if not profile:
            return redirect("/create_profile")
        profile = profile[0]
        return render_template("profile.html", username=username, role=role, profile=profile, issues=issues)



# Create Profile
@app.route("/create_profile", methods=["GET", "POST"])
@login_required
def create_profile():
    id = session["user_id"]
    info = db.execute("SELECT * FROM users WHERE id=?", id)[0]
    username = info["username"]
    role = info["role"]
    if role: role = "(Mechanic)"
    else: role = "(Customer)"

    if request.method == "POST":
        display_name = request.form.get("display_name")
        bio = request.form.get("bio")
        email = request.form.get("email")
        location_id = request.form.get("location_id")

        if not display_name or not bio or not email or not location_id:
            flash("All fields are required!")
            return redirect("/create_profile")

        # Save to database logic
        try:
            db.execute(
                "INSERT INTO profiles (display_name, bio, email, user_id, location_id) VALUES (?, ?, ?, ?, ?)",
                display_name,
                bio,
                email,
                session["user_id"],
                location_id,
            )
            flash("Profile created successfully!")
            return redirect("/profile")
        except Exception as e:
            flash("Error creating profile: " + str(e))
            return redirect("/create_profile")

    # Fetch locations for the dropdown
    return render_template("create_profile.html", LOCATIONS=LOCATIONS, username=username, role=role)



# edit_profile
@app.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    id = session["user_id"]
    info = db.execute("SELECT * FROM users WHERE id=?", id)[0]
    username = info["username"]
    role = info["role"]
    if role: role = "(Mechanic)"
    else: role = "(Customer)"

    if request.method == "GET":
        profile = db.execute("""SELECT
                profiles.display_name AS display_name,
                profiles.bio AS bio,
                profiles.email AS email,
                profiles.location_id AS location_id,
                locations.name AS location
            FROM profiles JOIN locations ON profiles.location_id=locations.id
            WHERE profiles.user_id = ?;
        """, id)[0]
        locations = db.execute("SELECT * FROM locations;")
        if not profile: return redirect("/create_profile")
        return render_template("edit_profile.html", profile=profile, LOCATIONS=LOCATIONS, username=username, role=role)
    else:
        display_name = request.form.get("display_name")
        bio = request.form.get("bio")
        email = request.form.get("email")
        location_id = int(request.form.get("location_id"))
        db.execute("""
            UPDATE profiles
            SET display_name = ?, bio = ?, email = ?, location_id = ?
            WHERE user_id = ?;
        """, display_name, bio, email, location_id, id)
        flash("Profile updated successfully!")
        return redirect("/profile")



# SEE ISSUES
@app.route("/issues", methods=["GET", "POST"])
@login_required
def issues():
    id = session["user_id"]
    info = db.execute("SELECT * FROM users WHERE id=?", id)[0]
    username = info["username"]
    role = info["role"]
    if role: role = "(Mechanic)"
    else: role = "(Customer)"

    if request.method == "GET":
        issues = db.execute('''SELECT
            issues.id AS issue_id,
            issues.title AS issue_title,
            issues.body AS issue_body,
            issues.status AS issue_status,
            issues.user_id AS issue_user_id,
            users.username AS user_name,
            profiles.display_name AS profile_display_name,
            profiles.bio AS profile_bio,
            profiles.email AS profile_email,
            locations.name AS location_name,
            locations.id AS location_id
        FROM
            issues
        JOIN
            users ON issues.user_id = users.id
        JOIN
            profiles ON users.id = profiles.user_id
        JOIN
            locations ON profiles.location_id = locations.id''')
        return render_template("issues.html", username=username, role=role, issues=issues, LOCATIONS=LOCATIONS)# The user will enter a status, either solved, or unsolved or all and a location
    else:
        status = int(request.form.get("status"))
        location = int(request.form.get("location"))
        issues = db.execute('''SELECT
            issues.id AS issue_id,
            issues.title AS issue_title,
            issues.body AS issue_body,
            issues.status AS issue_status,
            issues.user_id AS issue_user_id,
            users.username AS user_name,
            profiles.display_name AS profile_display_name,
            profiles.bio AS profile_bio,
            profiles.email AS profile_email,
            locations.name AS location_name,
            locations.id AS location_id
        FROM
            issues
        JOIN
            users ON issues.user_id = users.id
        JOIN
            profiles ON users.id = profiles.user_id
        JOIN
            locations ON profiles.location_id = locations.id
                            WHERE issues.status=? AND location_id=?;''', status, location)
        return render_template("issues.html", username=username, role=role, issues=issues, LOCATIONS=LOCATIONS)



# create_issues
@app.route("/create_issue", methods=["GET", "POST"])
@login_required
def create_issue():
    id = session["user_id"]
    info = db.execute("SELECT * FROM users WHERE id=?", id)[0]
    username = info["username"]
    role = info["role"]
    if role: role = "(Mechanic)"
    else: role = "(Customer)"

    if request.method == "GET":
            # show the person the field to select issues..they will enter the title and body
            return render_template("create_issue.html", username=username, role=role)
    else:
        title = request.form.get("title")
        body = request.form.get("body")
        status = 0
        db.execute("""
            INSERT INTO issues (title, body, status, user_id)
            VALUES (?, ?, ?, ?);
        """, title, body, status, id)
        flash("Issue created successfully!")
        return redirect("/profile")



# edit_issues
@app.route("/edit_issue", methods=["GET", "POST"])
@login_required
def edit_issue():
    id = session["user_id"]
    info = db.execute("SELECT * FROM users WHERE id=?", id)[0]
    username = info["username"]
    role = info["role"]
    if role: role = "(Mechanic)"
    else: role = "(Customer)"

    if request.method == "GET":
        issue_id = int(request.args.get("issue_id"))
        issue = db.execute("SELECT id, title, body, status FROM issues WHERE id=?", issue_id)[0]
        return render_template("edit_issues.html", username=username, role=role, issue=issue)

    else:
        title = request.form.get("title")
        body = request.form.get("body")
        issue_id = int(request.form.get("issue_id"))
        status = int(request.form.get("status"))
        db.execute("""
            UPDATE issues
            SET title = ?, body = ?, status=?
            WHERE id = ?;
        """, title, body, status, issue_id)
        flash("Issue updated successfully!")
        return redirect("/profile")



# LOG OUT
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()
    # Redirect user to login form
    flash("You have logged out")
    return redirect("/")
