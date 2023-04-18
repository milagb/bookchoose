from flask import render_template, request, redirect, session, flash, url_for
from bookchoose import app, db
from models import Books, Users

@app.route("/")
def index():
    book_list = Books.query.order_by(Books.id)
    return render_template('list.html', titulo='BookChoose', books = book_list)

@app.route("/new")
def new_book():
    if 'user_logged' not in session or session['user_logged'] == None:
        return redirect(url_for('login', proxima=url_for('new_book')))
    return render_template('new.html', titulo='New Book')

@app.route("/create", methods=['POST',])
def create():
    name = request.form['name']
    author = request.form['author']
    year_publication = request.form['year']
    
    book = Books.query.filter_by(name=name).first()
    if book:
        flash('The book already exists')
        return redirect(url_for('index'))
    
    new_book = Books(name=name, author=author, year_publication=year_publication)
    db.session.add(new_book)
    db.session.commit()

    return redirect(url_for('index'))

@app.route("/edit/<int:id>")
def edit(id):
    if 'user_logged' not in session or session['user_logged'] == None:
        return redirect(url_for('login', proxima=url_for('edit')))
    
    book = Books.query.filter_by(id=id).first()
    return render_template('edit.html', titulo='Edit Book', book = book)

@app.route("/update", methods=['POST',])
def update():
    book = Books.query.filter_by(id=request.form['id']).first()
    book.name = request.form['name']
    book.author = request.form['author']
    book.year_publication = request.form['year']

    db.session.add(book)
    db.session.commit()

    return redirect(url_for('index'))


@app.route("/login")
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima = proxima)

@app.route("/autenticate", methods=['POST',])
def autenticate():
    user = Users.query.filter_by(nickname=request.form['user']).first()
    if user:
        if request.form['password'] == user.password:
            session['user_logged'] = user.nickname
            flash(user.nickname + ' successfully logged in!')
            proxima_page = request.form['proxima']
            return redirect(proxima_page)
        else:
            flash('User not logged in')
            return redirect(url_for('login'))

@app.route("/logout")
def logout():
    session['user_logged'] = None
    flash('Successfully log out')
    return redirect(url_for('index'))