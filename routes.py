from flask_login import login_user, login_required, logout_user, current_user

from app import app, db
from flask import render_template, request, redirect, url_for
from sqlalchemy.exc import IntegrityError

from models import User, Text
from misc.translate import translate
from misc.separate import tokenize



@app.route('/')
def index():
    return render_template("index.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        username = request.form.get('login')
        password = request.form.get('password')
        if username and password:
            user = User.query.filter_by(username=username).first()
            print(user)
            if not user:
                return render_template('errorpage.html', error="THIS USER DOES NOT EXIST!")
            if password == user.password:
                login_user(user)
                return render_template('index.html')
            else:
                return render_template('errorpage.html', error="USERNAME OR PASSWORD IS WRONG")
        else:
            return render_template('errorpage.html', error="FILL BOTH FIELDS!")


@app.route('/register', methods=["GET", "POST"])
def register_user():
    if request.method == "GET":
        return render_template('register.html')
    else:
        username = request.form.get('login')
        password1 = request.form.get('password')
        password2 = request.form.get('password2')
        if password1 == password2:
            new_user = User(username=username, password=password1)
            try:
                db.session.add(new_user)
                db.session.commit()
            except IntegrityError as e:
                return render_template('errorpage.html', error=e)
            return render_template("index.html")
        else:
            return render_template('errorpage.html', error="PASSWORDS ARE NOT EQUAL")


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/add_text')
@login_required
def add_text():
    return render_template('add_text.html')


@app.route('/handle_text', methods=["POST"])
@login_required
def handle_text():
    header = request.form.get('header').strip()
    level = request.form.get('level')
    text = request.form.get('main_text').strip()
    translated_text = translate(text).strip()

    return render_template('edit_text.html',
                           text=text,
                           translated_text=translated_text,
                           header=header,
                           level=level)


@app.route('/save_text', methods=["POST"])
@login_required
def save_text():
    header = request.form.get('header').strip()
    text = request.form.get('text').strip()
    level = request.form.get('level')
    translation = request.form.get('translation').strip()
    # TODO: ADD VALIDATORS TO A FORM
    new_text = Text(header=header,
                    text=text,
                    translation=translation,
                    level=level,
                    user_id=current_user.id)
    db.session.add(new_text)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/all_texts')
def show_all_texts():
    texts = Text.query.order_by(Text.date.desc())
    return render_template('view_texts.html',
                           texts=texts)


@app.route('/text/id-<textid>')
def load_text(textid: int):

    post = Text.query.filter_by(id=int(textid)).first()
    tokenized_text = tokenize(post.text)
    return render_template('view_single_text.html',
                           post=post,
                           tokens=tokenized_text)