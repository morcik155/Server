import os
from flask import Flask, render_template, request, redirect, flash, session
from werkzeug.utils import secure_filename
import databese2
import datetime
import data.timetables

databese2.create_table_articles()
databese2.create_table_accounts()
databese2.create_table_day('5a', 'test')
databese2.create_table_day('5b', 'test')
databese2.create_table_day('6a', 'test')
databese2.create_table_day('6a', '"03.10.2022"')
databese2.create_table_day('6b', 'test')
databese2.create_table_day('7a', 'test')
databese2.create_table_day('7b', 'test')

app = Flask(__name__)
UPLOAD_FOLDER = 'data/files'
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
        session['class'] = False
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
            return render_template('admin/admin_home.html', login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
        if session['login']:
            return render_template('home.html', login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
        else:
            return render_template('home.html', login_h='/login', login_t='Войти', text='', disable='pointer-events: none')


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if session['login']:
            return redirect('/')
    except:
        session['login'] = False
        session['admin'] = False
        session['class'] = False
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        accounts = databese2.read('accounts', 'accounts')
        for i in accounts:
            if i[:-2] == (login, password):
                print(f'пользователь {login} успешпо вошёл в систему под поролем {password}')
                session['login'] = True
                session['name'] = login
                session['class'] = i[2]
                if i[-1] == 'True':
                    session['admin'] = True
                return redirect('/')
            else:
                print(f'попытка с данными {login} и {password} не удалась')

    return render_template('login.html', login_h='/login', login_t='Войти', text='Выложить ДЗ', disable='')


@app.route('/news', methods=['GET', 'POST'])
def news():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
        session['class'] = False
    data = databese2.read('articles', 'articles')
    if session['admin']:
        return render_template('admin/admin_news.html', login_h='/account', login_t=session['name'], data=data, text='Выложить ДЗ', disable='')
    if session['login']:
        return render_template('news.html', login_h='/account', login_t=session['name'], data=data, text='Выложить ДЗ', disable='')
    else:
        return render_template('news.html', login_h='/login', login_t='Войти', data=data, text='', disable='pointer-events: none')


@app.route('/news/add', methods=['GET', 'POST'])
def add_news():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
        session['class'] = False
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        file = request.files.getlist('file')
        filenames = ''
        for i in file:
            if i.filename == '':
                flash('No selected file')
                return redirect(request.url)
            if i:
                filename = secure_filename(i.filename)
                filenames = filenames + ' ' + filename
                i.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        f = open('id.txt', 'r')
        t = f.read()
        f.close()
        f = open('id.txt', 'w')
        f.write(str(int(t) + 1))
        f.close()
        databese2.add_article(t, title, text, '1')
        print(title, title, filenames)
    if session['admin']:
        return render_template('admin/admin_add.html', login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    if session['login']:
        return render_template('add.html', login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    else:
        return render_template('add.html', login_h='/login', login_t='Войти', text='', disable='pointer-events: none')


@app.route('/about')
def about():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
        session['class'] = False
    if session['admin']:
        return render_template('admin/admin_about.html', login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    if session['login']:
        return render_template('about.html', login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    else:
        return render_template('about.html', login_h='/login', login_t='Войти', text='', disable='pointer-events: none')


@app.route('/account', methods=['GET', 'POST'])
def account():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
        session['class'] = False
    if request.method == 'POST':
        logout = request.form['index']
        if logout == '1':
            session['login'] = False
            session['admin'] = False
            session['name'] = None
            session['class'] = False
            return redirect('/')
    if session['admin']:
        return render_template('admin/admin_account.html', login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    if session['login']:
        return render_template('account.html', login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    else:
        return redirect('/login')


@app.route('/news/<string:id>')
def new(id):
    data = databese2.read('articles', 'articles')
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
        session['class'] = False
    for i in data:
        if str(i[0]) == id:
            if session['admin']:
                return render_template('admin/admin_new.html', title=i[1], text=i[2], login_h='/account', login_t=session['name'], text2='Выложить ДЗ', disable='')
            if session['login']:
                return render_template('new.html', title=i[1], text=i[2], login_h='/account', login_t=session['name'], text2='Выложить ДЗ', disable='')
            else:
                return render_template('new.html', title=i[1], text=i[2], login_h='/login', login_t='Войти', text2='', disable='pointer-events: none')
        if session['admin']:
            return render_template('admin/admin_new.html', title='Такой статьи не существует', login_h='/account',login_t=session['name'], text='Выложить ДЗ', disable='')
        if session['login']:
            return render_template('new.html', title='Такой статьи не существует', login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
        else:
            return render_template('new.html', title='Такой статьи не существует', login_h='/login', login_t='Войти', text='', disable='pointer-events: none')


@app.route('/table')
def ed():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
        session['class'] = False
    data = []
    d = databese2.read(f'data_{session["class"]}', 'test')
    d1 = d[0][0][:-8]
    d2 = d[0][0][6:]
    d3 = d[0][0][3:-5]
    date = datetime.datetime(int(d2), int(d3), int(d1))
    while True:
        try:
            dd1 = ''
            dd2 = ''
            if len(str(date.day)) == 1:
                dd1 = '0' + str(date.day)
            else:
                dd1 = str(date.day)
            if len(str(date.month)) == 1:
                dd2 = '0' + str(date.month)
            else:
                dd2 = str(date.month)
            data.append(databese2.read(f'data_{session["class"]}', f'"{dd1}.{dd2}.{date.year}"'))
            date = date + 1
        except:
            break
    if session['admin']:
        return render_template('admin/admin_table.html', data=data, login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    if session['login']:
        return render_template('table.html', data=data, login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    else:
        return render_template('not_login/table.html', login_h='/login', login_t='Войти')


@app.route('/table/add')
def add_ed():
    try:
        if session['login']:
            pass
    except:
        session['login'] = False
        session['admin'] = False
        session['class'] = False
    if session['admin']:
        return render_template('admin/admin_tadd.html', data=None, login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    if session['login']:
        return render_template('tadd.html', data=None, login_h='/account', login_t=session['name'], text='Выложить ДЗ', disable='')
    else:
        return render_template('not_login/tadd.html', login_h='/login', login_t='Войти')




if __name__ == '__main__':
    app.run(debug=True, port=80, host='192.168.0.100')
