from flask import Flask, render_template, request, url_for, session, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'adk#dkjf'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cloud:2022db!UW@dbprivate.gwdemo.net/bulletin'
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://sanramon:2022db!UW@db.gwdemo.net/bulletin'
'''
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Users(db.Model):
    username = db.Column('username',db.String(20), primary_key = True)
    password = db.Column('password',db.String(20))
    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/index', methods=['GET'])
def index():
   if 'username' in session:
      session['logged'] = 'yes'
      return '<a href="%s">Logged in, you can transfer money</a>' % url_for('account') + '<br>' + "<b><a href = '/logout'>Log out</a></b>"
   return "You are not logged in <br> <a href = '/login'></b>" + "Log in</b></a>"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        tUsername = request.form['username']
        tPassword = request.form['password']
        tUser = Users.query.filter_by(username=tUsername).first()
        if tUser is not None and tUser.password == tPassword:
            session['username'] = request.form['username']
            print(tUser.username + " is logged in")
        else:
            print(tUsername + ", wrong input or password")
        return redirect(url_for('index'))
    return '''
   <form action = "" method = "post">
      <p> Username <input type = text name = "username"></p>
      <p> Password <input type = text name = "password"></p>
      <p><input type = submit value = Login></p>
   </form>
   '''

@app.route('/logout')
def logout():
   session.pop('username', None)
   return redirect(url_for('index'))

@app.route('/account', methods=['POST','GET'])
def account():
    if 'logged' not in session:
        return 'Please log in first!'
    if request.method == 'POST':
        if(request.form.get('select') == 'Transfer'):
            response = request.form.get('sender') + " successfully transferred" + " $" + request.form.get('amount') + " to " + request.form.get('recipient') + " through " + request.form.get('account')
        else:
            response = request.form.get('sender') + " successfully requested" + " $" + request.form.get('amount') + " from " + request.form.get('recipient') + " through " + request.form.get('account')
        return '<h1>Transaction Complete: ' + response + '</h1>' + '<a href="%s">Go back</a>' % url_for('account')
    return render_template("bank.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
