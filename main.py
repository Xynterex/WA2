import sqlite3
from datetime import datetime, timedelta

from flask import Flask, redirect, render_template, request

app = Flask(__name__)

conn = sqlite3.connect("taekwondo_pt_tracker.db")
cursor = conn.cursor()

# check all tables (so that I don't have to bloody redownload the db file)
cursor.execute("SELECT * FROM Account_Detail;")
print("Account_Detail: ", cursor.fetchall())
cursor.execute("SELECT * FROM Physical_Training;")
print("Physical_Training: ", cursor.fetchall())
cursor.execute("SELECT * FROM PtDesc;")
print("PtDesc: ", cursor.fetchall())
cursor.execute("SELECT * FROM PtReps;")
print("PtReps: ", cursor.fetchall())
cursor.execute("SELECT * FROM AccountPT;")
print("AccountPT: ", cursor.fetchall())


# runtime variables
exco_pin = "3829"
login_message = "Welcome!"
signup_message = "Welcome!"
acc_id = None
acc_message = ""

@app.route('/')
def home():
    return render_template("login.html", login_message=login_message)

@app.route("/signup")
def signup():
    return render_template("signup.html", signup_message=signup_message)


@app.route("/store", methods=["POST"])
def store():
    global signup_message
    global login_message

    name = request.form.get("name")
    password = request.form.get("password")
    status = request.form.get("status")
    pin = request.form.get("pin", "")

    # open Account_Detail table
    cursor.execute("SELECT * FROM Account_Detail;")
    details = cursor.fetchall()
    
    for row in details:
        if row[1] == name:
            signup_message = "Username already exists!"
            return redirect("/signup")

    # password validation done in frontend

    if status == "exco" and pin != exco_pin:
        signup_message = "Exco PIN is incorrect."
        return redirect("/signup")

    # update Account_Detail table
    account_detail = (name, password, status)
    cursor.execute("""
        INSERT INTO Account_Detail (name, pswd, status)
        VALUES (?, ?, ?);""", account_detail)
    conn.commit()

    cursor.execute("SELECT acc_id FROM Account_Detail WHERE name = ?;", (name,))
    acc_id = cursor.fetchone()[0]

    # add existing PT into AccountPT table
    cursor.execute("SELECT * FROM Physical_Training;")
    pt_list = cursor.fetchall()
    now = datetime.now().date()
    for row in pt_list:
        pt_id = row[0]
        end_date = datetime.strptime(row[5], "%Y-%m-%d").date()
        print("now",now)
        print("end",end_date)
        if end_date >= now:
            account_pt = (acc_id, pt_id)
            cursor.execute("""
                INSERT INTO AccountPT (acc_id, pt_id)
                VALUES (?, ?);""", account_pt)
    
    conn.commit()
    
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

    # open Account_Detail table
    cursor.execute("SELECT * FROM Account_Detail;")
    details = cursor.fetchall()
    
    for row in details:
        if row[1] == name and row[2] == password and row[3] == status:
            # update account id to import matching data from db
            global acc_id
            acc_id = row[0]
            # redirect to accounts

            # open AccountPT table and add the pt_id from Physical_Training table

            return redirect("/account")

    # no matching name and password and status
    login_message = "Login failed!"
    return redirect("/")

# LOGGED IN

@app.route("/account")
def account():
    # protection from just typing in the url
    global acc_id
    if acc_id == None:
        return redirect("/")

    # get account details
    cursor.execute("SELECT * FROM Account_Detail WHERE acc_id = ?", (acc_id,))
    account_detail = cursor.fetchall()
    name = account_detail[0][1]
    status = account_detail[0][3]

    # account message
    global acc_message
    if acc_message == "":
        acc_message = f"Welcome {name}!"

    # prepare data for pt table
    cursor.execute("SELECT pt_id FROM AccountPT WHERE acc_id = ?", (acc_id,))
    pt_ids = cursor.fetchall()
    pt_ids = tuple([row[0] for row in pt_ids])
    print("pt_id")
    print(pt_ids)
    if len(pt_ids) == 0:
        pt_details = []
        pt_descs = []
        pt_reps = []
    else:
        if len(pt_ids) == 1:
            # time to SQL inject
            pt_ids = f"({pt_ids[0]})"
        # get physical training data
        cursor.execute(f"SELECT * FROM Physical_Training WHERE pt_id IN {pt_ids}")
        pt_details = cursor.fetchall()
        # get pt desc data
        pt_descs = []
        cursor.execute("SELECT pt_id FROM PtDesc")
        desc_ids = tuple([row[0] for row in cursor.fetchall()])
        print(desc_ids)
        for pt_id in pt_ids:
            if pt_id in desc_ids:
                cursor.execute("SELECT description FROM PtDesc WHERE pt_id = ?", (pt_id,))
                print("cursor")
                pt_desc = cursor.fetchall()[0][0]
                print(pt_desc)
                pt_descs.append(pt_desc)
            else:
                pt_descs.append("No Description")
        '''
        cursor.execute(f"SELECT description FROM PtDesc WHERE pt_id IN {pt_ids}")
        pt_desc = cursor.fetchall()
        for i in range(len(pt_desc)):
            if pt_desc[i][0] == None:
                pt_desc[i] = ""
            else:
                pt_desc[i] = pt_desc[i][0]
        '''
        # get pt reps data
        pt_reps = []
        cursor.execute("SELECT pt_id FROM PtReps")
        reps_ids = tuple([row[0] for row in cursor.fetchall()])
        print(reps_ids)
        for pt_id in pt_ids:
            if pt_id in reps_ids:
                cursor.execute("SELECT Reps FROM PtReps WHERE pt_id = ?", (pt_id,))
                print("cursor")
                pt_rep = cursor.fetchall()[0][0]
                print(pt_rep)
                pt_reps.append(pt_rep)
            else:
                pt_reps.append("No Reps")
            
    print(pt_details)
    print(pt_descs)
    print(pt_reps)
    table = []
    # process the 3 lists into a 2D list and return to template
    for i in range(len(pt_details)):
        table.append(list(pt_details[i][0:3]) + [pt_reps[i]] + [pt_descs[i]] + list(pt_details[i][4:6]))
        
    print(table)
    return render_template("account.html", name=name, status=status, acc_message=acc_message, table=table)


@app.route("/submit_pt", methods=["POST"])
def submit_pt():
    global acc_message
    pt_id = request.form.get("completed_id")
    if pt_id == "NULL":
        acc_message = "No physical training selected."
        return redirect("/account")
        
    date_submitted = datetime.now()
    cursor.execute("SELECT end_date FROM Physical_Training WHERE pt_id = ?", (pt_id,))
    print("end date")
    date_due = datetime.strptime(cursor.fetchall()[0][0], "%Y-%m-%d")
    date_diff = (date_due - date_submitted).days
    if date_diff < 0:
        # passed deadline
        acc_message = "You have passed the deadline!"
    else:
        acc_message = "Good job and get some rest!"

    # remove row from AccountPT
    global acc_id
    print("acc_id")
    print(acc_id)
    print("pt_id")
    print(pt_id)
    cursor.execute("DELETE FROM AccountPT WHERE pt_id = ? AND acc_id = ?", (pt_id, acc_id))
    conn.commit()

    return redirect("/account")


@app.route("/set_pt")
def set_pt():
    global acc_message
    pt_name = request.args.get("pt_name")
    pt_desc = request.args.get("pt_desc", "")
    pt_sets = request.args.get("pt_sets")
    pt_reps = request.args.get("pt_reps", "")
    pt_duration = request.args.get("pt_duration")

    # validate no duplicate PT
    cursor.execute("SELECT pt_name FROM Physical_Training")
    pt_names = cursor.fetchall()
    for row in pt_names:
        if row[0] == pt_name:
            acc_message = f"Physical Training {pt_name} already exists!"
            return redirect("/account")

    # store dates
    pt_startdate = datetime.now().date()
    pt_enddate = pt_startdate + timedelta(days=int(pt_duration))
    pt_startdate = pt_startdate.strftime("%Y-%m-%d")
    pt_enddate = pt_enddate.strftime("%Y-%m-%d")
    
    # store name, sets and duration into Physical_Training table
    cursor.execute("""
    INSERT INTO Physical_Training (pt_name, pt_sets, pt_duration, start_date, end_date)
    VALUES (?, ?, ?, ?, ?)""", (pt_name, pt_sets, pt_duration, pt_startdate, pt_enddate))
    # retrieve pt_id
    cursor.execute("""SELECT pt_id FROM Physical_Training
    WHERE pt_name = ?""", (pt_name,))
    pt_id = cursor.fetchall()[0][0]
    # store pt_desc
    if pt_desc != "":
        cursor.execute("""
        INSERT INTO PtDesc (pt_id, description)
        VALUES (?, ?)""", (pt_id, pt_desc))

    # store pt_reps
    if pt_reps != "":
        cursor.execute("""
        INSERT INTO PtReps (pt_id, Reps)
        VALUES (?, ?)""", (pt_id, pt_reps))

    # update AccountPT table
    cursor.execute("SELECT acc_id FROM Account_Detail")
    acc_ids = cursor.fetchall()
    for row in acc_ids:
        id = row[0]
        cursor.execute("""
        INSERT INTO AccountPT (acc_id, pt_id)
        VALUES (?, ?)""", (id, pt_id))
        
    conn.commit()

    acc_message = "Physical Training added successfully!"
    return redirect("/account")

@app.route("/logout")
def logout():
    global acc_id
    global login_message
    acc_id = None
    login_message = "Successfully Logged Out!"
    
    return redirect("/")

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000)