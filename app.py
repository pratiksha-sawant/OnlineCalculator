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


class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


users = [User(id=1, username='user1', password="user1"), User(id=2, username='user2', password="user2")]


@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if session['user_id'] == x.id][0]
        g.user = user


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)  # removes the current session if same user tries to login again
        username = request.form['username']
        password = request.form['password']
        user = [x for x in users if x.username == username][0]  # select the correct user

        if user and user.password == password:
            session['user_id'] = user.id
            return redirect(url_for('home'))  # if method post start the user session

        return redirect(url_for('login'))  # if there's any error just return the login page

    return render_template('login.html')  # if method get just return the login page


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template('home.html')


if __name__ == "__main__":
    app.run(debug=True)
