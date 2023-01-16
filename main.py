from flask import Flask,render_template,request,url_for,redirect,flash,session
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_session import Session


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'Fastag'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login',methods=["GET","POST"])
def login():
    cur = mysql.connection.cursor()
    if request.method=="POST":
        ent_email = request.form.get("email")
        ent_password = request.form.get("password")
        print(ent_email)
        print(ent_password)
        cur.execute(f"select *from owner where email_id='{ent_email}'")
        data_login = cur.fetchone()
        if data_login and data_login['password']==ent_password:
            session["email"]=ent_email
            return redirect(url_for("user"))
        else:
            flash("Wrong credentials")
            return redirect(url_for("login"))
        #print(email in emails)   
    return render_template("login.html")
@app.route('/logout')
def logout():
    session["email"]=None
    return redirect(url_for("login"))

@app.route('/user')
def user():
    cur=mysql.connection.cursor()
    emailId = session.get("email")
    cur.execute(f"SELECT * from owner where email_id = '{emailId}'")
    user = cur.fetchone()
    reg_no = user['reg_no']
    cur.execute(f"SELECT new_balance from transaction where reg_no = '{reg_no}' order by date_added desc limit 1")
    bal = cur.fetchone()
    return render_template("user.html",user=user,bal=bal)

@app.route('/pricing')
def pricing():
    return render_template("pricing.html")

@app.route('/table')
def table():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * from transaction")
    transactions = cur.fetchall()
    print(transactions) 
    return render_template("table.html",transactions=transactions)

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        uid = request.form.get("Userid")
        reg=request.form.get("Regno")
        fastag=request.form.get("fastag_id")
        Name = request.form.get("Name")
        Phone = request.form.get("Phone")
        email = request.form.get("email")
        password = request.form.get("password")
        cur = mysql.connection.cursor()
        cur.execute("INSERT into owner(user_id,reg_no,fastag_id,name,phone,email_id,password) values (%s,%s,%s,%s,%s,%s,%s)",(uid,reg,fastag,Name,Phone,email,password))
        cur.execute("select * from owner")
        mysql.connection.commit()
        flash("Registered Succesfully")
        return redirect(url_for("login"))
    return render_template("register.html")    

@app.route('/transaction',methods=['GET','POST'])
def transaction():
    if request.method=="POST":
        reg=request.form.get("Reg_no")
        fastag=request.form.get("fastag_id")
        toll_id = request.form.get("toll_id")
        toll_loc = request.form.get("toll_location")
        parking_id = request.form.get("parking_id")
        parking_loc = request.form.get("parking_Location")
        cur = mysql.connection.cursor()
        cur.execute(f"SELECT new_balance from transaction where reg_no = {reg} order by date_added desc limit 1")
        bal = cur.fetchone()
        if toll_id=="":
            dec = 50
        else:
            dec = 100
        if bal is None:
            old_bal = 1000
        else:
            old_bal = bal["new_balance"]
        new_bal = old_bal -dec
        cur.execute("INSERT into transaction(reg_no,fastag_id,toll_id,toll_location,parking_id,parking_location,old_balance,new_balance) values (%s,%s,%s,%s,%s,%s,%s,%s)",(reg,fastag,toll_id,toll_loc,parking_id,parking_loc,old_bal,new_bal))
        cur.execute("select * from transaction")
        mysql.connection.commit()
        return redirect(url_for("user"))
    return render_template("transaction.html")

if __name__== "__main__":
    app.run(debug=True) 
    
    
# UPDATE transaction
# SET NEW.new_balance = NEW.old_balance - CASE WHEN  NEW.toll_id = '' THEN 50 ELSE 100 END
# WHERE transaction_id = NEW.transaction_id;
