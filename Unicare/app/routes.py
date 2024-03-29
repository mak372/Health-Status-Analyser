from flask import render_template, url_for, flash, request, redirect
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm, DocRegistrationForm, DocLoginForm
from app.models import User, Doctor
from flask_login import login_user, current_user, logout_user
import sqlite3 as sql

colors = [
    "#F7464A", "#46BFBD", "#FDB45C", "#FEDCBA",
    "#ABCDEF", "#DDDDDD", "#ABCABC", "#4169E1",
    "#C71585", "#FF4500", "#FEDCBA", "#46BFBD"]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(fullname=form.fullname.data, email=form.email.data, tel=form.tel.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/admindashboard")
def admindashboard():
    return render_template('admindashboard.html',title='Admin dashboard')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Log in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/docregister", methods=['GET', 'POST'])
def docregister():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = DocRegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        doctor = Doctor(fullname=form.fullname.data, email=form.email.data, tel=form.tel.data, password=hashed_password)
        db.session.add(doctor)
        db.session.commit()
        flash('Your account has been created! You can now log in', 'success')
        return redirect(url_for('doclogin'))
    return render_template('docregister.html', title='Register', form=form)


@app.route("/doclogin", methods=['GET', 'POST'])
def doclogin():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        doctor = Doctor.query.filter_by(email=form.email.data).first()
        if doctor and bcrypt.check_password_hash(doctor.password, form.password.data):
            login_user(doctor, remember=form.remember.data)
            flash('Log in successfully!', 'success')
            return redirect(url_for('admindashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('doclogin.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('home'))


@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html', title='Dashboard')



@app.route("/assess")
def assess():
    return render_template('assessment.html', title='Self Assessment Test')

@app.route("/selftest",methods=["GET","POST"])
def selftest():
    comp = []
    resp = request.form.getlist('meet')
    for i in resp:
        comp.append(int(i))
    result = sum(comp)
    if result >= 50:
        return render_template("highrisk.html")
    elif result < 50:
        return render_template("lowrisk.html")	

@app.route("/medicalhistory")
def medhistory():
    return render_template('medhistory.html',title='Medical history')

@app.route("/meddata",methods=["GET","POST"])
def meddata():
    name = request.form["name"]
    age = request.form["age"]
    email = request.form["email"]
    phone = request.form["phone"]
    blood = request.form["blood"]
    gender = request.form["gender"]
    comor = request.form["diab"]
    specs = request.form["specs"]
    age = int(age)
    phone = int(phone)
    with sql.connect("medhistory.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO history(name,age,email,phone,blood,gender,comor,specs) VALUES(?,?,?,?,?,?,?,?)",
                    (name,age,email,phone,blood,gender,comor,specs))
        con.commit()
    flash('Details recorded successfully','success')
    return render_template("dashboard.html")
    con.close()
    
@app.route("/viewprofile",methods=["GET","POST"])
def viewprofile():
    profile = request.form["conf"]
    con = sql.connect("medhistory.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM history WHERE name = ?",(profile,))
    rows = cur.fetchall()
    if len(rows) == 0:
        return render_template("medhistory.html")
    else:
        return render_template("viewprofile.html",rows=rows)
    con.close()

@app.route("/admincheck",methods=["GET","POST"])
def admincheck():
    patientid = request.form["patientid"]
    con = sql.connect("medhistory.db")
    con.row_factory = sql.Row
    cur = con.cursor()
    cur.execute("SELECT * FROM history WHERE ID = ?",(patientid,))
    rows = cur.fetchall()
    return render_template("admincheck.html",rows=rows,patientid=patientid)
    con.close()

@app.route("/diagnosis",methods=["GET","POST"])
def diagnosis():
    return render_template("patientdiagnosis.html")

@app.route("/healthcare",methods=["GET","POST"])
def healthcare():
    name = request.form["name"]
    symptoms = request.form["symptoms"]
    bdate = request.form["bdate"]
    date = request.form["date"]
    month = request.form["month"]
    tests = request.form["tests"]
    diagnosis = request.form["diagnosis"]
    with sql.connect("admin.db") as con:
        cur = con.cursor()
        cur.execute("INSERT INTO admin (name,symptoms,bday,visit,diagmonth,tests,diagnosis) VALUES(?,?,?,?,?,?,?)",
                    (name,symptoms,bdate,date,month,tests,diagnosis))
        con.commit()
    return render_template("admindashboard.html")
    con.close()

@app.route("/viewdata",methods=["GET","POST"])
def viewdata():
    diag = request.form["diag"]
    labels = ['January','February','March','April','May','June','July','August','September','October','November','December']
    values = []
    con = sql.connect("admin.db")
    con.row_factory = sql.Row 
    cur = con.cursor()
    cur.execute("SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='January' UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='February' UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='March' UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='April' UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='May'UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='June'UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='July'UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='August'UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='September'UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='October'UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='November'UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='November'UNION ALL SELECT COUNT(diagnosis) FROM admin WHERE diagnosis=? AND diagmonth='December'",(diag,diag,diag,diag,diag,diag,diag,diag,diag,diag,diag,diag,diag,))
    rows = cur.fetchall()
    for row in rows:
        values.append(row[0])
    line_labels = labels
    line_values = values
    return render_template('bar_chart.html',title='Patient Statistics',max=10,labels=line_labels,values=line_values,disease=diag)
    con.close()

