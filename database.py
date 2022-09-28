import sqlite3


def create_table_accounts():
    try:
        sqlite_connection = sqlite3.connect('data/Server_data.db')
        sqlite_create_table_query = '''CREATE TABLE accounts (
                                        name TEXT NOT NULL,
                                        password TEXT NOT NULL);'''
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def create_table_HomeTasks():
    try:
        sqlite_connection = sqlite3.connect('data/Server_data.db')
        sqlite_create_table_query = '''CREATE TABLE HomeTasks (
                                        id INTEGER PRIMARY KEY,
                                        date TEXT NOT NULL,
                                        text TEXT NOT NULL,
                                        sub TEXT NOT NULL,
                                        who_reduct TEXT NOT NULL);'''
        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Таблица SQLite создана")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def add(table, data: list):
    try:
        sqlite_connection = sqlite3.connect('data/Server_data.db')
        f = open(f'data/last_id_{table}.txt', 'r')
        id = int(f.read())
        f.close()
        f = open(f'data/last_id_{table}.txt', 'w')
        f.write(f'{id + 1}')
        f.close()
        f = open(f'data/last_id_{table}.txt', 'r')
        id = f.read()
        f.close()
        data.insert(0, id)
        if table == "accounts":
            cursor = sqlite_connection.cursor()
            print("База данных подключена к SQLite")
            cursor.executemany("INSERT INTO accounts VALUES (?,?,?)", (data,))
            sqlite_connection.commit()
            print("Значения успешно добавленны")
        elif table == "HomeTasks":
            cursor = sqlite_connection.cursor()
            print("База данных подключена к SQLite")
            cursor.executemany("INSERT INTO HomeTasks VALUES (?,?,?,?,?)", (data,))
            sqlite_connection.commit()
            print("Значения успешно добавленны")
            cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def delete(table, id):
    try:
        sqlite_connection = sqlite3.connect('data/Server_data.db')

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(f"""DELETE FROM {table} WHERE id = {id}""")
        sqlite_connection.commit()
        print("Значения успешно удалены")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def edit(table, user, new_password):
    try:
        sqlite_connection = sqlite3.connect('data/Server_data.db')
        sqlite_create_table_query = f"""
                                        UPDATE {table}
                                        SET password = '{new_password}',
                                        WHERE name = '{user}'
                                        """

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Значения успешно изменены")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def edit_dz(id, new_dz, user):
    try:
        sqlite_connection = sqlite3.connect('data/Server_data.db')
        sqlite_create_table_query = f"""
                                        UPDATE HomeTasks
                                        SET text = '{new_dz}',
                                        WHERE id = '{id}',
                                        SET hwo_reduct = '{user}',
                                        WHERE id = {id}
                                        """

        cursor = sqlite_connection.cursor()
        print("База данных подключена к SQLite")
        cursor.execute(sqlite_create_table_query)
        sqlite_connection.commit()
        print("Значения успешно изменены")

        cursor.close()

    except sqlite3.Error as error:
        print("Ошибка при подключении к sqlite", error)
    finally:
        if (sqlite_connection):
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")


def read(table):
    try:
        sqlite_connection = sqlite3.connect('data/Server_data.db')
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