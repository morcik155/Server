import datetime
import os
from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
from databese2 import *
import time

create_table_articles()
create_table_accounts()
create_table_day('5a', 'test')
create_table_day('5b', 'test')
create_table_day('6a', 'test')
create_table_day('6b', 'test')
create_table_day('7a', 'test')
create_table_day('7b', 'test')

app = Flask(__name__)
UPLOAD_FOLDER = 'static/files'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = '43758962823456'


@app.route('/', methods=['GET', 'POST'])
def main():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
    if request.method == 'POST':
        if request.method == 'POST':
            if 'file' not in request.files:
                flash('No file part')
                return redirect(request.url)
            file = request.files['file']
            if file.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if file:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return redirect('/')
    else:
        if session['admin']:
            return render_template('admin/admin_home.html', login_h='/account', login_t=session['name'])
        if session['login']:
            return render_template('home.html', login_h='/account', login_t=session['name'])
        else:
            return render_template('home.html', login_h='/login', login_t='Войти')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session['login']:
            return redirect('/')
    except:
        session['login'] = False
        session['admin'] = False
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        accounts = read('accounts', 'accounts')
        for i in accounts:
            if i[:-2] == (login, password):
                print(f'пользователь {login} успешпо вошёл в систему под поролем {password}')
                session['login'] = True
                session['name'] = login
                if i[-1] == 'True':
                    session['admin'] = True
                return redirect('/')
            else:
                print(f'попытка с данными {login} и {password} не удалась')

    return render_template('login.html', login_h='/login', login_t='Войти')


@app.route('/news', methods=['GET', 'POST'])
def news():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
    data = read('articles', 'articles')
    if session['admin']:
        return render_template('admin/admin_news.html', login_h='/account', login_t=session['name'])
    if session['login']:
        return render_template('news.html', login_h='/account', login_t=session['name'], data=data)
    else:
        return render_template('news.html', login_h='/login', login_t='Войти', data=data)


@app.route('/news/add')
def add_news():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
    if session['admin']:
        return render_template('admin/admin_add.html', login_h='/account', login_t=session['name'])
    if session['login']:
        return render_template('add.html', login_h='/account', login_t=session['name'])
    else:
        return render_template('add.html', login_h='/login', login_t='Войти')


@app.route('/about')
def about():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
    if session['admin']:
        return render_template('admin/admin_about.html')
    return render_template('about.html')


@app.route('/account', methods=['GET', 'POST'])
def account():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
    if request.method == 'POST':
        logout = request.form['index']
        if logout == '1':
            session['login'] = False
            session['admin'] = False
            session['name'] = None
            return redirect('/')
    if session['login']:
        return render_template('account.html')
    else:
        return redirect('/login')


@app.route('/news/<id:String>')
def new(id):
    pass


if __name__ == '__main__':
    app.run(debug=True, port=80, host='192.168.0.100')
