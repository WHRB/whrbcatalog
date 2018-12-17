"""
Helper functions
"""

from functools import wraps
from flask import redirect, render_template, session


def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(string):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            string = string.replace(old, new)
        return string
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(wrapped_func):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(wrapped_func)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return wrapped_func(*args, **kwargs)
    return decorated_function
