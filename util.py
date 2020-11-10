import csv
import urllib.request

from flask import redirect, render_template, request, session, url_for
from functools import wraps

from webs import *

def apology(top="", bottom=""):
    """Renders message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
            ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=escape(top), bottom=escape(bottom))

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.11/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect(url_for("login", next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def lookup(driver, symbol):
    if symbol == "NA":
        return {
        "symbol": 'NA',
        "name": 'NO',
        "price": float(0)
        }
    
    return getQuote(driver, symbol)

def usd(value):
    """Formats value as USD."""
    return "${:,.2f}".format(value)
