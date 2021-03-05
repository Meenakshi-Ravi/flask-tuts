from flask import Flask, render_template, request, redirect, url_for, session
from flask_mail import Mail,Message
import pyodbc
import smtplib
import re

app = Flask(__name__)
app.secret_key = 'your secret key'
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-67SG5599;'
                      'Database=logindb;'
                      'Trusted_Connection=yes;')



app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = "meenu97.ravi@gmail.com"
app.config['MAIL_PASSWORD'] = "test1234%"
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)



@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template("index.html")


@app.route('/list/<emptype>/<email>', methods=['GET'])
def emplist(emptype, email):
    if emptype == "admin":
        cursor = conn.cursor()
        cursor.execute(
            "select * from dbo.employee where usertype = 'employee' ")
        account = cursor.fetchall()
    if emptype == "employee":
        cursor = conn.cursor()
        cursor.execute(
            "select * from dbo.employee where emailid = '" + email + "' ")
        account = cursor.fetchall()
    return render_template("list.html", data=account, emptype=emptype)


@app.route('/login', methods=['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'GET':
        return render_template('login.html', msg=msg)
    if request.method == 'POST' and 'emailid' in request.form and 'password' in request.form:
        print("here")
        emailid = request.form['emailid']
        password = request.form['password']
        cursor = conn.cursor()
        cursor.execute(
            ''' select * from dbo.employee where emailid = ? and password = ?''', [emailid, password])
        account = cursor.fetchone()
        if account:
            session["emailid"] = account.emailid
            session["usertype"] = account.usertype
            return redirect(url_for("emplist", emptype=account.usertype, email=account.emailid))
        else:
            msg = 'Incorrect username / password !'
    return render_template('login.html', msg=msg)


@app.route('/logout')
def logout():
    session.pop('usertype', None)
    session.pop('emailid', None)
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    msg = ''
    if session['usertype'] != "admin":
        return redirect(url_for("login"))
    if request.method == 'GET':
        return render_template('register.html', msg=msg)
    if request.method == 'POST' and 'emailid' in request.form and 'password' in request.form and 'name' in request.form and 'usertype' in request.form and 'dateofbirth' in request.form and 'qualification' in request.form and 'state' in request.form and 'postalcode' in request.form and 'experience' in request.form:
        print("here")
        emailid = request.form['emailid']
        password = request.form['password']
        name = request.form['name']
        usertype = request.form['usertype']
        dateofbirth = request.form['dateofbirth']
        qualification = request.form['qualification']
        state = request.form['state']
        postalcode = request.form['postalcode']
        experience = request.form['experience']
        cursor = conn.cursor()
        cursor.execute(
            '''select * from dbo.employee where emailid = ?''', [emailid, ])
        account = cursor.fetchone()
        print(account)
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z0-9]+', usertype):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[0-9]+[-]+', dateofbirth):
            msg = 'must be in dd-mm-yyyy format'
        elif not re.match(r'[A-Za-z0-9]+', qualification):
            msg = "required"
        elif not re.match(r'[A-Za-z0-9]+', state):
            msg = "required"
        elif not re.match(r'[0-9]+', postalcode):
            msg = "required"
        elif not re.match(r'[0-9]+', experience):
            msg = "required"
        elif not emailid or not name or not state:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('''insert into dbo.employee VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''', [
                           emailid, password, name, usertype, dateofbirth, qualification, state, postalcode, experience])
            conn.commit()
            msg = 'You have successfully registered !'
    elif request.method == 'POST':
        msg = 'Please fill out the form !'
    return render_template('register.html', msg=msg)


@app.route("/update", methods=["GET"])
def update():
    if session['usertype'] != "admin":
        return redirect(url_for("login"))
    email = request.args.get("email")
    print(email)
    cursor = conn.cursor()
    cursor.execute("select * from dbo.employee where emailid = '"+email+"'")
    account = cursor.fetchone()
    print(list(account))
    return render_template("update.html", data=account)


@app.route("/updatedetails", methods=['POST'])
def updatedetails():
    if session['usertype'] != "admin":
        return redirect(url_for("login"))
    msg = ''
    if request.method == 'POST' and 'emailid' in request.form and 'password' in request.form and 'name' in request.form and 'usertype' in request.form and 'dateofbirth' in request.form and 'qualification' in request.form and 'state' in request.form and 'postalcode' in request.form and 'experience' in request.form:
        print("here")
        emailid = request.form['emailid']
        password = request.form['password']
        name = request.form['name']
        usertype = request.form['usertype']
        dateofbirth = request.form['dateofbirth']
        qualification = request.form['qualification']
        state = request.form['state']
        postalcode = request.form['postalcode']
        experience = request.form['experience']

        if not re.match(r'[^@]+@[^@]+\.[^@]+', emailid):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', password):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z0-9]+', name):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[A-Za-z0-9]+', usertype):
            msg = 'Username must contain only characters and numbers !'
        elif not re.match(r'[0-9]+[-]+', dateofbirth):
            msg = 'must be in dd-mm-yyyy format'
        elif not re.match(r'[A-Za-z0-9]+', qualification):
            msg = "required"
        elif not re.match(r'[A-Za-z0-9]+', state):
            msg = "required"
        elif not re.match(r'[0-9]+', postalcode):
            msg = "required"
        elif not re.match(r'[0-9]+', experience):
            msg = "required"
        elif not emailid or not name or not state:
            msg = 'Please fill out the form !'
        else:
            cursor = conn.cursor()
            cursor.execute("update dbo.employee set password='"+password+"',  name='"+name+"',  dateofbirth='"+dateofbirth+"',  qualification='" +
                           qualification+"',  state='"+state+"',  postalcode='"+postalcode+"',  experience="+experience+" where emailid ='"+emailid+"'")
            conn.commit()
            msg = 'You have successfully updated !'
    return  redirect(url_for("emplist", emptype=session['usertype'], email=session['emailid']))


@app.route("/delete", methods=["GET"])
def delete():
    if session['usertype'] != "admin":
        return redirect(url_for("login"))
    id = request.args.get("id")
    print(id)
    cursor = conn.cursor()
    cursor.execute("delete from dbo.employee where id = '"+id+"'")
    conn.commit()
    return redirect(url_for("emplist", emptype=session['usertype'], email=session['emailid']))

@app.route("/send_message", methods=["GET","POST"])
def send_message():
    email = request.form.get("email")
    msg = "Hello man"
    message = Message(sender="meenu97.ravi@gmail.com", recipients=[email])
    message.body = msg
    mail.send(message)
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("meenu1997.ravi@gmail.com", "test1234%")
    server.sendmail("meenu1997.ravi@gmail.com", email, msg)
    success = "Message Sent"
    return render_template("result.html", success=success)


if __name__ == "__main__":
    app.run(debug=True)
