from flask import Flask, flash, redirect, render_template, request, session, url_for
from util import *
from fileh import *

app = Flask(__name__)

from selenium import webdriver
chromdriver = "C:\\Users\\vinay.yadav\\Downloads\\chromedriver"
driver = webdriver.Chrome(chromdriver)


@app.route("/")
@login_required
def index():
    # check if portfolio table exists and/or if user owns any stocks
    try:
        stocks = getStocks()
    
    except:
        return apology("U don't own any stocks", "cheapskate")
        
    numSharesTotal = []
        
    for stock in stocks:
        numSharesTotal.append(stock["numShares"])
        
    totalShares = sum(numSharesTotal)
    
    if totalShares == 0:
        return apology("U don't own any stocks", "penny pincher")
             
    currentPrices = []
    currentValues = []
    
    bal = getBal()
    cash = bal['bal']

    # find current value for each owned stock
    for stock in stocks:
        currentPrice = lookup(driver, stock["symbol"])
        currentPrice = currentPrice["price"]
        currentPrices.append(currentPrice)
        currentValue = currentPrice * stock["numShares"]
        currentValues.append(currentValue)
        
    totalPrice = sum(currentValues)
    totalValue = cash + totalPrice

    # render index.html with portfolio information
    return render_template("index.html", stocks = stocks, \
    cash = cash, \
    currentPrices = currentPrices, 
    currentValues = currentValues, \
    totalValue = totalValue)
    
    
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Must provide username")

        # ensure password was submitted
        elif not request.form.get("password"):
            return apology("Must provide password")

        # only one user for now
        rows = {"username":"smriti", "password":"12345"}

        # ensure username exists and password is correct
        if request.form.get("password") == "12345":
            print(request.form.get("password"))
        if request.form.get("password") != rows["password"] or request.form.get("username") != rows["username"]:
            return apology("invalid username and/or password")
        
        # remember which user has logged in
        session["user_id"] = rows["username"]

        # redirect user to home page
        return redirect(url_for("index"))

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        print("vinay is back")
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for("login"))
    
    
    
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""
    
    # if user reached route via POST(as by submitting a form via POST)
    if request.method == "POST":
    
        # ensure username was submitted
        if not request.form.get("username"):
            return apology("Username required.")
    
        # ensure password was submitted
        if not request.form.get("password"):
            return apology("Password required.")
        
        # make sure passwords match, else apoligize
        if not request.form.get("password") == request.form.get("confirm"):
            return apology("Passwords do not match.")
        
        # add user to database if username unique, hash password
        result = "vinay"
        if not result:
            return apology("That username is taken.")
            
        else:
            # keep them logged in
            session["user_id"] = result
            
            # redirect user to home page
            return redirect(url_for("index"))
    
    # else user reached route via GET
    else:
        return "Under Construction"
        return render_template("register.html")
 
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    
    # if user reached route via POST(as by submitting a form via POST)
    if request.method == "POST":
        
        quote = lookup(request.form.get("symbol"))
    
        if quote == None:
            return apology("Please try another symbol")
           
        else:
            # pull values from dict, quote
            return render_template("quoted.html", name = quote['name'], price = usd(quote['price']), symbol = quote['symbol'])
            
    # else user reached route via GET
    else:
        return "Under Construction"
        return render_template("quote.html")


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""
    
    # if user reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
    
        # ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")
            
        # ensure # of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares to buy")
            
        shares = request.form.get("shares")
            
        # ensure number of shares is positive
        if int(shares) <= 0:
            return apology("you must buy atleast 1 share")
            
        # get dict named rows that includes price, name, and symbol values
        stock = lookup(driver, request.form.get("symbol"))
    
        if stock == None:
            return apology("that symbol doesn't exist")
            
        # find out if user has anough money to buy stock
        else:
            
            #variables
            cash = getBal()
            value = stock["price"] * int(shares)
            remaining_cash = cash["bal"] - value
            
            if not remaining_cash or remaining_cash <= 0:
                return apology("you too po' to buy this stock")
                
            else:
                
                stocks = getStocks()
                stock['numShares'] = int(shares)
                stock['stockName'] = stock['name'] 
                stocks.append(stock)
                storeStocks(stocks)
                # update remaining cash amount in table, users
                
                c = {}
                c['bal'] = remaining_cash
                storeBal(c)
                
                # redirect user to home page showing current portfolio of stocks
                return redirect(url_for("index"))
            
    # else if user reached route via GET (as by clicking a link or via redirect)

    else:
        return render_template("buy.html")

 
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    if request.method == "POST":
    
        # ensure stock symbol was submitted
        if not request.form.get("symbol"):
            return apology("must provide stock symbol")
            
        # ensure # of shares was submitted
        if not request.form.get("shares"):
            return apology("must provide number of shares to buy")
            
        shares = request.form.get("shares")
            
        # ensure number of shares is positive
        if int(shares) <= 0:
            return apology("you must buy atleast 1 share")
            
        # get dict named rows that includes price, name, and symbol values
        stock = lookup(driver, request.form.get("symbol"))
    
        if stock == None:
            return apology("that symbol doesn't exist")
            
        # find out if user has anough money to buy stock
        else:
            
            #variables
            cash = getBal()
            value = stock["price"] * int(shares)
            remaining_cash = cash["bal"] + value
            
            if  int(shares)<= 0:
                return apology("you too po' to buy this stock")
                
            else:
                
                stocks = getStocks()
                stock['numShares'] =  - int(shares)
                stocks.append(stock)
                storeStocks(stocks)
                # update remaining cash amount in table, users
                
                c = {}
                c['bal'] = remaining_cash
                storeBal(c)
                
                # redirect user to home page showing current portfolio of stocks
                return redirect(url_for("index"))
            
    # else if user reached route via GET (as by clicking a link or via redirect)

    else:
        return render_template("buy2.html")

''' 
@app.route("/sellaaa", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""
    
    # if user reached route via POST(as by submitting a form via POST)
    if request.method == "POST":
        
        if request.form.get("portfolioSell") == None:
            return apology("Portoflio ID required")
        
        # variables
        portfolioSell = int(request.form.get("portfolioSell"))
        symbolSell = request.form.get("symbolSell").upper()
        
        # ensure symbol was submitted
        if not symbolSell:
            return apology("Symbol required")
            
        # get username from users 
        userCheck = db.execute("SELECT username FROM users WHERE id = :id", id = session["user_id"])

        # ensure all form data submitted is correct per sql table data
        checks = db.execute("SELECT portfolioID, stockName, symbol, numShares, valuePurchase, pricePerShare, buyer FROM portfolio WHERE buyer = :username AND portfolioID = :portfolioID AND numShares > :numShares", \
        username = userCheck[0]["username"], \
        portfolioID = portfolioSell, \
        numShares = 0)
        
        if not checks:
            return apology("portfolio ID is", "INCORRECT")
        
        if symbolSell != checks[0]["symbol"]:
            return apology("symbols do not match")
            
        # update cash and insert sold data into tables
        cash = db.execute("SELECT cash FROM users WHERE id = :id", \
        id = session['user_id'])
        
        # look up current stock price
        currentPrice = lookup(symbolSell)
        
        # get sold stock total value
        currentValue = currentPrice["price"] * checks[0]["numShares"]
        
        #figure profit or loss from sale
        valuePurchase = checks[0]["valuePurchase"]
        profit = float(valuePurchase) - currentValue
        sharesSold = checks[0]["numShares"]
            
        # update cash in user table
        db.execute("UPDATE users SET cash = :cash WHERE id = :id", \
        cash = currentValue + cash[0]["cash"], \
        id = session['user_id'])
        
        profitPerShare = checks[0]["pricePerShare"] - currentPrice["price"]
        
        # update portfolio table with sold data (date, value, shares)
        db.execute("UPDATE portfolio SET soldDate = :soldDate, sharesSold = :sharesSold, numShares = :numShares, valueSold = :valueSold, \
        profitLoss = :profitLoss WHERE buyer = :buyer AND portfolioID = :portfolioID", \
        soldDate = now, \
        sharesSold = sharesSold, \
        numShares = 0, \
        valueSold = "{:,.4f}".format(currentValue), \
        profitLoss = "{:,.2f}".format(profit), \
        buyer = userCheck[0]["username"], \
        portfolioID = portfolioSell)
    
        # create sold.html to display sold info
        return render_template("sold.html", numShares = sharesSold, symbol = symbolSell, stockName = checks[0]["stockName"], profit = profitPerShare)
    
    # else user reached route via GET
    else:
        name = db.execute("SELECT username FROM users WHERE id = :id", id = session["user_id"])
    
        # check if portfolio table exists and/or if user owns any stocks
        try:
            stocks = db.execute("SELECT buyer, numShares FROM portfolio WHERE buyer = :buyer AND numShares > 0", \
            buyer = name[0]["username"])
        
        except:
            return apology("can't sell what U don't own")
            
        numSharesTotal = []
            
        for stock in stocks:
            numSharesTotal.append(stock["numShares"])
            
        totalShares = sum(numSharesTotal)
        
        if totalShares == 0:
            return apology("U don't own any stocks", "tightwad")
            
        stocks = db.execute("SELECT portfolioID, stockName, symbol, numShares, pricePerShare, valuePurchase, purchaseDate FROM portfolio WHERE buyer = :buyer AND numShares > 0 ORDER BY purchaseDate", \
        buyer = name[0]["username"])
        
        currentPrices = []
        currentValues = []
        profits = []

        cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
        
        # find current value for each owned stock
        for stock in stocks:
            currentPrice = lookup(stock["symbol"])
            currentPrice = currentPrice["price"]
            currentPrices.append(round(currentPrice, 4))
            currentValue = currentPrice * stock["numShares"]
            currentValues.append(round(currentValue, 4))
            pf = currentPrice - stock["pricePerShare"]
            profits.append(round(pf, 4))
            
        totalPrice = sum(currentValues)
        totalValue = "{:,.2f}".format(cash[0]["cash"] + totalPrice)
        
        # render index.html with portfolio information
        return render_template("sell.html", stocks = stocks, \
        cash = "{:,.2f}".format(cash[0]["cash"]), \
        currentPrices = currentPrices, \
        currentValues = currentValues, \
        totalValue = totalValue, \
        profits = profits)
        
        return render_template("sell.html")
'''
        
        
@app.route("/addFunds", methods=["GET", "POST"])
@login_required
def addFunds():
    """Allow user to increase funds in account."""
    return "Under Construction"
    cash = db.execute("SELECT cash FROM users WHERE id = :id", id = session["user_id"])
    
    cash = cash[0]["cash"]
    
    # if user reached route via POST(as by submitting a form via POST)
    if request.method == "POST":
        
        # process increased funding
        if request.form.get("amount") == None:
            return apology("Try again")
            
        amount = int(request.form.get("amount"))
        
        db.execute("UPDATE users SET cash = :cash", \
        cash = cash + amount)
        
        cash = cash + amount
        
        return render_template("fundsAdded.html", cash = cash)
        
    else:
        return "Under Construction"
        return render_template("addFunds.html", cash = cash)
        

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""
    return "Under Construction"
    name = db.execute("SELECT username FROM users WHERE id = :id", id = session["user_id"])
    
    # check if portfolio table exists (if user has bought/sold any stocks)
    try:
        buys = db.execute("SELECT symbol, stockName, purchaseDate, valuePurchase, sharesPurchased FROM portfolio WHERE buyer = :buyer", \
        buyer = name[0]["username"])
    
    except:
        return apology("trade some stocks", "already")
        
    sells = db.execute("SELECT symbol, stockName, soldDate, valueSold, sharesSold, profitLoss FROM portfolio WHERE buyer = :buyer AND sharesSold > :sharesSold", \
        buyer = name[0]["username"], \
        sharesSold = 0)
        
    if sells == None:
        return render_template("history.html", buys = buys)
        
    else:
        
        return render_template("history.html", buys = buys, sells = sells)
 
if __name__ == "__main__":
    #app.run()
#    f = open("./db/tmp.txt", "w+")
    
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(host='0.0.0.0', port=80)