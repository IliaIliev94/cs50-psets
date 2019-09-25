import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

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


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

os.environ["API_KEY"] = "pk_a5b91e3cdf7f4f7da2c221900a9be509"


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Initiliaze the variable to hold the sum of the cash available to the user and his total holdings in stocks
    total = 0.00

    # Load the users stocks into a variable
    stocks = db.execute(
        "SELECT symbol, name, SUM(shares) AS shares, price  FROM portfolio WHERE id = :user GROUP BY symbol", user=session["user_id"])

    # Iterate over the user's portfolio
    for row in stocks:

        # Get the current price of the stock
        row["price"] = lookup(row["symbol"])["price"]

        # Add each stock's total price to the total variable
        total += row["price"] * row["shares"]

        # Assign each stock's total price formatted in usd currency to the total column
        row["TOTAL"] = usd(row["shares"] * row["price"])

        # Convert each stock's price into usd format
        row["price"] = usd(row["price"])

    # Get the users cash from the database
    cash = db.execute("SELECT cash FROM users WHERE id = :user", user=session["user_id"])

    # Add the users cash to the total variable
    total += cash[0]["cash"]

    # Load the index page and pass the variables to it
    return render_template("index.html", stocks=stocks, cash=usd(cash[0]["cash"]), total=usd(total))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Submit the form via POST and get the input values
    if request.method == "POST":
        symbol = request.form.get("symbol")
        try:
            shares = int(request.form.get("shares"))
        except:
            return apology("PLEASE INPUT WHOLE NUMBER")

        # Check the user input
        if not symbol:
            return apology("Stock symbol musn't be blank")
        elif int(shares) < 1:
            return apology("Number of shares has to be at least 1")

        # Check the price of the stock and the cash the user has left
        stock = lookup(symbol)
        if not stock:
            return apology("INVALID SYMBOL")
        userCash = db.execute("SELECT cash from users WHERE id = :session", session=session["user_id"])
        totalPrice = stock["price"] * shares

        # Check if user has eough cash to buy shares
        if userCash[0]["cash"] < totalPrice:
            return apology("Not enough cash to buy shares")
        else:
            db.execute("UPDATE users SET cash = :usercash WHERE id = :session",
                       usercash=userCash[0]["cash"] - totalPrice, session=session["user_id"])
            db.execute("INSERT INTO portfolio(id, symbol, name, shares, price) VALUES(:id, :symbol, :name,  :shares, :price)",
                       id=session["user_id"], symbol=symbol.upper(), name=stock["name"], shares=shares, price=stock["price"])

        return redirect("/")
        # Check the stocks price
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    """Return true if username available, else false, in JSON format"""
    if request.method == "GET":
        username = request.args.get("username")
        names = db.execute("SELECT username FROM users WHERE username = :username", username=username)
        print(names)
        if len(username) > 0 and not names:
            print("202-Success")
            return jsonify(True)
        else:
            return jsonify(False)


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    portfolio = db.execute("SELECT symbol, shares, price, date FROM portfolio WHERE id = :id", id=session["user_id"])
    return render_template("history.html", portfolio=portfolio)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

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
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    # Check the request method. If it is a get request return the quote.html page
    if request.method == 'GET':
        return render_template('quote.html')

    # If the request method is post get the symbol that the user has entered. If he has not return an apology.
    else:
        symbol = request.form.get("symbol")
        if not symbol:
            return apology("Symbol can't be blank")

        # Check if the symbol is valid. If it is return a table with the requested symbol's information.
        else:
            quote = lookup(symbol)
            if not quote:
                return apology("INVALID SYMBOL")
            quote["price"] = usd(quote["price"])
            if not quote:
                return apology("INVALID SYMBOL")
            return render_template("quoted.html", quote=quote)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # Check the request method
    if request.method == "POST":

        # Get the data from the form
        name = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Hash the users password
        hash = generate_password_hash(password)

        # Check if any of the values are missing and if the password and confirmation match
        if not name:
            return apology("Username can't be blank")
        elif not password:
            return apology("Password can't be blank")
        elif password != confirmation:
            return apology("Passwords don't match")

        # Try to insert the users information into the database
        result = db.execute("INSERT into users(username, hash) values(:name, :hash)", name=name, hash=hash)

        # Check if the username is taken
        if not result:
            return apology("Username is taken")

        # Get the users ID and store it in the session dictionary
        id = db.execute("SELECT id FROM users WHERE username = :name", name=name)
        session["user_id"] = id[0]["id"]

    # If the request method is get return the register page.
    else:
        return render_template("register.html")

    return redirect("/")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    # Recieve the submitted data if the request method is post.
    if request.method == "POST":
        symbol = request.form.get("symbol")
        shares = int(request.form.get("shares"))
        stock = lookup(symbol)

        # Check the current amount of shares that the user has of this stock.
        currentShares = db.execute(
            "SELECT SUM(shares) as shares FROM portfolio WHERE id = :id and symbol = :symbol GROUP by symbol", id=session["user_id"], symbol=symbol)
        if currentShares[0]["shares"] < shares:
            return apology("TOO MANY SHARES")

        # If the user has enough shares to sell, insert the into the portfolio the current stock with the negative value of the shares that he has sold. Because the total number of shares on the homepage table are calculated with the sum function
        # this method will work.
        db.execute("INSERT INTO portfolio(id, symbol, name, shares, price) values(:id, :symbol, :name, :shares, :price)",
                   id=session["user_id"], symbol=stock["symbol"], name=stock["name"], shares=-shares, price=stock["price"])

        # Increase the users cash with the profit he has gained from selling the shares
        db.execute("UPDATE users SET cash = cash + :profit WHERE id = :id", profit=shares * stock["price"], id=session["user_id"])

        return redirect("/")

    # Show the user the sell form page if the request method is get.
    else:
        stocks = db.execute("SELECT symbol FROM portfolio WHERE id = :user GROUP BY symbol", user=session["user_id"])
        return render_template("sell.html", stocks=stocks)


@app.route("/password", methods=["GET", "POST"])
def password():
    # If the request method is post get the data from the form
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirm")

        # Check if the user exists in the database and if the password matches the confirmation
        name = db.execute("SELECT username FROM users WHERE username = :username", username=username)
        if password == confirmation and name:

            # If the user exists and the passwords match, change the users password to the new one.
            db.execute("UPDATE users SET hash = :password WHERE username = :username",
                       password=generate_password_hash(password), username=username)
            return redirect("/")

        # If the user doesn't exist or the passwords don't match return an apology
        else:
            return apology("INCORRECT USERNAME")

    # If the request method is get return the password.html page.
    else:
        return render_template("password.html")


@app.route("/cash", methods=["GET", "POST"])
def cash():
    if request.method == "POST":
        cash = int(request.form.get("cash"))
        if not cash:
            return apology("PLEASE PROVIDE THE AMOUNT BY WHICH YOU WANT TO INCREASE YOUR CASH")
        db.execute("UPDATE users SET cash = cash + :cash WHERE id=:id", cash=cash, id=session["user_id"])
        return redirect("/")

    else:
        return render_template("cash.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)