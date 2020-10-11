from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import desc
import random

app = Flask(__name__)
app.secret_key = 'abcdefghijklmnop'

ENV = 'dev'
if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/calculator'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Calculator(db.Model):
    __tablename__ = 'calculations'
    cal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    user_name = db.Column(db.String(20))
    num1 = db.Column(db.Float)
    num2 = db.Column(db.Float)
    operations = db.Column(db.String(20))
    signs = db.Column(db.String(20))
    answer = db.Column(db.Float)

    def __init__(self, user_id,user_name, num1, num2, operations, signs, answer):
        self.user_id = user_id
        self.user_name = user_name
        self.num1 = num1
        self.num2 = num2
        self.operations = operations
        self.signs = signs
        self.answer = answer


# user class to store login information
class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


# calculation class to create calculative objects

class Calculation:
    def __init__(self, num1, num2, operation):
        self.num1 = num1
        self.num2 = num2
        self.operation = operation

    def calculator(self):
        if self.operation == 'add':
            result = float(self.num1) + float(self.num2)
        elif self.operation == 'subtract':
            result = float(self.num1) - float(self.num2)
        elif self.operation == 'multiply':
            result = float(self.num1) * float(self.num2)
        else:
            result = float(self.num1) / float(self.num2)

        return result


user1 = User(id=1, username='user1', password="user1")
user2 = User(id=2, username='user2', password="user2")
users = [user1, user2]


# creating the session for each user
@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if session['user_id'] == x.id][0]
        g.user = user
        session['session_id'] = random.randint(100, 500)


# login page -> index page call
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)  # removes the current session if same user tries to login again
        username = request.form['username']
        password = request.form['password']
        user = [x for x in users if x.username == username][0]  # select the correct user

        if user and user.password == password:
            session['user_id'] = user.id
            session['user_name'] = user.username
            return redirect(url_for('home'))  # if method post start the user session

        return redirect(url_for('login'))  # if there's any error just return the login page

    return render_template('login.html')  # if method get just return the login page


# home page call for users
@app.route('/home', methods=['GET', 'POST'])
def home():
    operations_dict = {}
    if request.method == 'POST':
        num1 = request.form['num1']
        num2 = request.form['num2']
        operation = request.form['operation']

        if operation == 'add':
            opt = '+'
        elif operation == 'subtract':
            opt = '-'
        elif operation == 'multiply':
            opt = 'x'
        else:
            opt = '/'

        # print(operations_dict)
        if not num1 or not num2:
            num1 = 0
            num2 = 0

        # calculation the result
        values = Calculation(num1, num2, operation)
        result = values.calculator()

        # store the result in database
        data = Calculator(session['user_id'], session['user_name'], num1, num2, operation, opt, result)
        db.session.add(data)
        db.session.commit()

        # store the result in database
        # if session['user_id'] == user1.id:
        #     data1 = Calculator(user1.id, user1.username, num1, num2, operation, opt, result)
        #     db.session.add(data1)
        #     db.session.commit()
        # else:
        #     data2 = Calculator(user2.id, user2.username,  num1, num2, operation, opt, result)
        #     db.session.add(data2)
        #     db.session.commit()

        # display top 10 calculations by users on web page
        cl_result = db.session.query(Calculator).order_by(desc(Calculator.cal_id)).limit(10).all()
        for row in cl_result:
            operations_dict[row.cal_id] = [row.user_name, row.num1, row.num2, row.operations, row.signs, row.answer]

        return render_template('home.html', result=result, operations_dict=operations_dict)

    return render_template('home.html', operations_dict={session['user_name']: 0})


if __name__ == "__main__":
    app.run(debug=True)
