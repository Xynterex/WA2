from flask import Flask, render_template, url_for, request, redirect
import csv

app = Flask(__name__)

#runtime variables
exco_pin = "3829"
login_message = "Welcome!"
signup_message = "Welcome!"
authenticated = False

@app.route('/')
def home():
    global authenticated
    authenticated = False
    return render_template("login.html", login_message=login_message)

@app.route("/signup")
def signup():
    return render_template("signup.html", signup_message=signup_message)


@app.route("/store", methods=["POST"])
def store():
    print("hello")
    global signup_message
    global login_message

    name = request.form.get("name")
    password = request.form.get("password")
    status = request.form.get("status")
    pin = request.form.get("pin", "")
    
    # file closes after with block
    with open("account_details.csv", "r") as file:
        details = list(csv.reader(file))[1:]
        
    for row in details:
        if row[0] == name:
            signup_message = "Username already exists!"
            return redirect("/signup")
    print("hello")
    # password validation done in frontend

    if status == "exco" and pin != exco_pin:
        signup_message = "Exco PIN is incorrect."
        return redirect("/signup")

    # data validated
    # file closes after with block
    with open("account_details.csv", "a") as file:
        writer = csv.writer(file)
        writer.writerow([name, password, status])

    login_message = "Account created successfully!"
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    global login_message
    name = request.form.get("name")
    password = request.form.get("password")
    status = request.form.get("status")
    pin = request.form.get("pin", "")
    
    # reject wrong pin
    if status == "exco" and pin != exco_pin:
        login_message = "Exco PIN is incorrect."
        return redirect("/")

    # validate name and password
    # file closes after with block
    with open("account_details.csv", "r") as file:
        details = list(csv.reader(file))[1:]
    for row in details:
        if row[0] == name and row[1] == password and row[2] == status:
            # update global variable to allow use of account routes from login route
            global authenticated
            authenticated = True
            # redirect to accounts
            if status == "exco":
                return redirect(f"/exco/{name}")
            else:
                return redirect(f"/member/{name}")

    # no matching name and password and status
    login_message = "Login failed!"
    return redirect("/")

@app.route("/exco/<name>")
def exco(name):
    # protection from just typing in the url
    global authenticated
    if not authenticated:
        return redirect("/")
    return render_template("exco.html", name=name)

@app.route("/member/<name>")
def member(name):
    global authenticated
    if not authenticated:
        return redirect("/")
    return render_template("member.html", name=name)
if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)