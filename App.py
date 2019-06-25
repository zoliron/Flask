from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin

import ExcelRead
from LoginForm import LoginForm
from RegisterForm import RegisterForm
from Switch import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'R123r123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:\\Users\\user\\PycharmProjects\\Flask\\database.db'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Home route
@app.route('/')
@login_required
def index():
    return render_template('index.html')


# Signin route
@app.route('/signin', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('index'))

        return '<h1>Invalid username or password</h1>'
    return render_template('login.html', form=form)


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'

    return render_template('signup.html', form=form)


# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


# Dashboard route
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', name=current_user.username)


# Switch Commands route
@app.route('/switchCommandsRedirect')
@login_required
def switchCommandsRedirect():
    switches = ExcelRead.openExcel()
    return render_template('switchCommands.html', switches=switches)


# Login route
@app.route('/switchCommand', methods=['GET', 'POST'])
@login_required
def switchCommand():
    if request.form['ipAddress'] != '':
        print('Manual Switch')
        newSwitch = Switch(request.form['ipAddress'], request.form['username'], request.form['password'])
    else:
        print('List Switch')
        switchIp = str(request.form['selectedSwitch']).split(' - ')
        newSwitch = Switch(switchIp[1], request.form['username'], request.form['password'])
    command = request.form['command']
    if 'show log' in command:
        command = command + request.form['specificLog']
        print(command)
        output = newSwitch.sendCommand(command)
        if output == "Switch Authentication Failed":
            switches = ExcelRead.openExcel()
            return render_template('switchCommands.html', error=output, switches=switches)
        if output == "":
            return render_template('output.html', output='No Logs Found')
        return render_template('output.html', output=output)
    elif 'vrf' in command:
        if request.form['sxpVRF'] != "":
            command = command + request.form['sxpVRF']
        elif request.form['PingVRF'] != "" and request.form['pingVRFAddress'] != "":
            command = command + request.form['PingVRF'] + " " + request.form['pingVRFAddress']
        elif request.form['ArpVRF'] != "":
            command = command + request.form['ArpVRF']
        print(command)
        output = newSwitch.sendCommand(command)
        if output == "Switch Authentication Failed":
            switches = ExcelRead.openExcel()
            return render_template('switchCommands.html', error=output, switches=switches)
        if output == "":
            return render_template('output.html', output='Wrong VRF')
        return render_template('output.html', output=output)
    elif 'ping' in command:
        command = command + request.form['pingAddress']
        print(command)
        output = newSwitch.sendCommand(command)
        if output == "Switch Authentication Failed":
            switches = ExcelRead.openExcel()
            return render_template('switchCommands.html', error=output, switches=switches)
        if output == "":
            return render_template('output.html', output='No IP Address Inserted')
        return render_template('output.html', output=output)
    else:
        print(command)
        output = newSwitch.sendCommand(command)
        if output == "Switch Authentication Failed":
            switches = ExcelRead.openExcel()
            return render_template('switchCommands.html', error=output, switches=switches)
        return render_template('output.html', output=output)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
