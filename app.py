from flask import (
    Flask,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for
)

app = Flask(__name__)
app.secret_key = 'abcdefghijklmnop'


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


users = [User(id=1, username='user1', password="user1"), User(id=2, username='user2', password="user2")]


# creating the session for each user
@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if session['user_id'] == x.id][0]
        g.user = user


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
    if request.method == 'POST':
        num1 = request.form['num1']
        num2 = request.form['num2']
        operation = request.form['operation']
        operations_dict = {session['user_name']: [num1, num2, operation]}

        if not num1 or not num2:
            num1 = 0
            num2 = 0

        values = Calculation(num1, num2, operation)
        result = values.calculator()

        return render_template('home.html', result=result, operations_dict=operations_dict)

    return render_template('home.html', operations_dict={session['user_name']: 0})


if __name__ == "__main__":
    app.run(debug=True)
