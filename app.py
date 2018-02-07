# merged examples from the following to get a mssql based flask app with login / sessions:
## https://libraries.io/pypi/Flask-PyMssql
## https://github.com/shekhargulati/flask-login-example/blob/master/flask-login-example.py
# flask login documentation:
## http://flask-login.readthedocs.io/en/latest/

# for basic web api with flask / mssql
from flask import Flask, jsonify

# for logging in and more advanced flask functions
from flask_login import login_required, current_user, LoginManager, UserMixin, \
                            login_user, logout_user
from flask import request, url_for, render_template
import flask
from urlparse import urlparse, urljoin

from db import conn, dbRepo

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

def toJson(obj):
    if isinstance(obj, list):
        return jsonify([ [y.__dict__ for y in x] if isinstance(x,list) else x.__dict__ for x in obj])
    return obj.__dict__

@app.route('/date/<username>')
@login_required
def getdate(username):
    return toJson(dbRepo.date_get())

@app.route('/freedate')
def getfreedate():
    return toJson(dbRepo.date_get())

@app.route('/freeemail')
def getfreeemail():
    # cursor = conn.cursor(as_dict=True)
    # cursor.execute('SELECT GETDATE() AS TheDate;')
    # thedate = cursor.fetchone()
    # return jsonify(thedate)
    regs = dbRepo.Customer_get()
    print regs
    return toJson(dbRepo.Customer_get())

@app.route('/freetwo')
def getfreetwo():
    return toJson([dbRepo.date_get(), dbRepo.Customer_get()])

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route('/index')
@login_required
def index():
        return flask.render_template('index.html')

# silly user model
class User(UserMixin):
    def __init__(self, id):
        self.id = id
        self.name = "user" + str(id)
        self.password = self.name + "_secret"
    def __repr__(self):
        return "%d/%s/%s" % (self.id, self.name, self.password)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == username + "_secret":
            id = username
            user = User(id)
            login_user(user)
            flask.flash('Logged in successfully.')
            next = flask.request.args.get('next')
            if not is_safe_url(next):
                return flask.abort(400)
            return flask.redirect(next or flask.url_for('index'))
        else:
            return flask.abort(401)
    else:
        return flask.render_template('login.html')    

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return flask.redirect(flask.url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

