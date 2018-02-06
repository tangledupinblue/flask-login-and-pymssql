# merged examples from the following to get a mssql based flask app with login / sessions:
## https://libraries.io/pypi/Flask-PyMssql
## https://github.com/shekhargulati/flask-login-example/blob/master/flask-login-example.py
# flask login documentation:
## http://flask-login.readthedocs.io/en/latest/

# for basic web api with flask / mssql
from flask import Flask, jsonify
import pymssql

# for logging in and more advanced flask functions
from flask_login import login_required, current_user, LoginManager
from flask import request, url_for, render_template

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

server = '127.0.0.1'
user = 'bob'
password = 'bob'
database= 'tempdb'

#db = pymssql(app)

conn = pymssql.connect(server, user, password, database)

@app.route('/date/<username>')
@login_required
def getdate(username):
    cursor = conn.cursor(as_dict=True)
    cursor.execute('SELECT GETDATE() AS TheDate;')
    thedate = cursor.fetchone()
    return jsonify(thedate)

@app.route('/freedate')
def getfreedate():
    cursor = conn.cursor(as_dict=True)
    cursor.execute('SELECT GETDATE() AS TheDate;')
    thedate = cursor.fetchone()
    return jsonify(thedate)


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']        
        if password == username + "_secret":
            id = username.split('user')[1]
            user = User(id)
            flask.flash('Logged in successfully.')
            next = flask.request.args.get('next')
            if not is_safe_url(next):
                return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))
        else:
            return abort(401)
    else:
        return flask.render_template('login.html', form=form)    


if __name__ == '__main__':
    app.run(debug=True)
