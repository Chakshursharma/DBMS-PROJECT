from flask import Flask,render_template,request,url_for,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL(app)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'Fastag'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:root@localhost/fastag"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


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
        cur.execute("select *from owner")
        data_login = cur.fetchall()
        print(data_login)
        emails = {user['email_id'] for user in data_login}
        passwords = {user['password'] for user in data_login}
        for e in emails:
            if ent_email==e:
                for p in passwords:
                    if ent_password==p:
                        return redirect(url_for("user"))
                    else:
                        return redirect(url_for("index"))
            else:
                return redirect(url_for("index"))
        print(emails)
        #print(email in emails)
       

        
    return render_template("login.html")

@app.route('/user')
def user():
    return render_template("user.html")

@app.route('/pricing')
def pricing():
    return render_template("pricing.html")

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=="POST":
        uid = request.form.get("Userid")
        Name = request.form.get("Name")
        Phone = request.form.get("Phone")
        email = request.form.get("email")
        password = request.form.get("password")
        # if len(password)<6:
            # print("Too less ")  Add trigger
        cur = mysql.connection.cursor()
        cur.execute("INSERT into owner(user_id,name,phone,email_id,password) values (%s,%s,%s,%s,%s)",(uid,Name,Phone,email,password))
        cur.execute("select * from owner")
        mysql.connection.commit()
        return redirect(url_for("login"))
    return render_template("register.html")    

if __name__== "__main__":
    app.run(debug=True) 