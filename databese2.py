import sqlite3


def data(table, query):
    sqlite_connection = None
    try:
        sqlite_connection = sqlite3.connect(f'data/{table}.db')
        sqlite_create_table_query = query
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Операция прошла успешно")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def create_table_accounts():
    data('accounts', 'CREATE TABLE accounts (name TEXT NOT NULL, password TEXT NOT NULL, class TEXT, status TEXT);')


def create_table_articles():
    data('articles', 'CREATE TABLE articles (id INTEGER NOT NULL UNIQUE, name NOT NULL UNIQUE, text TEXT, files TEXT);')


def create_table_day(class_, day):
    data(f'data_{class_}', f'CREATE TABLE {day} (subject TEXT NOT NULL UNIQUE, text TEXT, who_reduct TEXT NOT NULL );')


def edit_accounts(user, password):
    data('accounts', f"UPDATE accounts SET password = '{password}', WHERE name = '{user}'")


def edit_article(name, text, files):
    data(
        'articles' f"UPDATE articles SET text ='{text}', WHERE name = '{name}', SET files = '{files}', WHERE name = '{name}'")


def edit_day(class_, day, subject, text, who_reduct):
    data(f'data_{class_}',
         f"UPDATE {day} SET text = '{text}', WHERE subjext = '{subject}', SET who_reduct = '{who_reduct}, WHERE subject = '{subject}'")


def add_account(name, password, class_):
    data('accounts' f"INSERT INTO accounts VALUES ({name}, {password}, {class_})")


def add_article(id, name, text, files):
    data('articles' f"INSERT INTO articles VALUES ({id}, {name}, {text}, {files})")


def add_day(subject, text, who_reduct):
    data('accounts' f"INSERT INTO accounts VALUES ({subject}, {text}, {who_reduct})")


def read(base, table):
    try:
        sqlite_connection = sqlite3.connect(f'data/{base}.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sqlite_select_query = f"""SELECT * from {table}"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        cursor.close()
        return records


    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def delete_article(base, table, name):
    data(base, f"DELETE FROM {table} WHERE name = {name}")


def delete_accounts(base, table, name):
    data(base, f"DELETE FROM {table} WHERE name = {name}")


def delete_subject(base, table, subject):
    data(base, f"DELETE FROM {table} WHERE subject = {subject}")
