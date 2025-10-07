import secrets
import string
from flask import Flask, render_template, request, send_from_directory
import random
import nltk

nltk.download('words')
from nltk.corpus import words

app = Flask(__name__)

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

@app.route("/", methods=["GET", "POST"])
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
    )

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(app.root_path, 'favicon.ico', mimetype='image/vnd.microsoft.icon')

if __name__ == "__main__":
    app.run(debug=True)
