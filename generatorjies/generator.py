import secrets
import string
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import functools

app = Flask(__name__)
app.config['SECRET_KEY'] = 'very_secret_key'

users = {
    "admin": {'password': generate_password_hash("admin")},
    "1": {'password': generate_password_hash("1")},
}

def generate_password(length, complexity):
    if complexity == "Низкая":
        characters = string.ascii_lowercase
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password

    if complexity == "Средняя":
        characters = string.ascii_letters + string.digits
    elif complexity == "Высокая":
        characters = string.ascii_letters + string.digits + string.punctuation
    else:
        characters = string.ascii_lowercase

    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return view(**kwargs)
    return wrapped_view

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    password = ""
    length = 12
    complexity = "Средняя"

    if request.method == "POST":
        try:
            length = int(request.form.get("length"))
            complexity = request.form.get("complexity")

            if length <= 0:
                password = "Длина пароля должна быть больше 0"
            else:
                password = generate_password(length, complexity)

        except ValueError:
            password = "Неверный формат длины"

    return render_template(
        "index.html",
        password=password,
        length=length,
        complexity=complexity,
        username = session.get('username')
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        user = users.get(username)

        if user is None:
            error = 'Неверный логин.'
        elif not check_password_hash(user['password'], password):
            error = 'Неверный пароль.'

        if error is None:
            session.clear()
            session['username'] = username
            return redirect(url_for('index'))

        flash(error)

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/favicon.ico')
def favicon():
    return app.send_static_file('favicon.ico')

if __name__ == "__main__":
    app.run(debug=True)
