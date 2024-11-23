from flask import redirect, render_template, session
from functools import wraps
import json


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function

def check(username, password):
    if not username:
        return False
    elif not password:
        return False
    return True

def read_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)


def write_json(data, file_path):
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)  # indent=4 makes the JSON file more readable

def is_mechanic(role):
    if not role: return True

M = 1
C = 0