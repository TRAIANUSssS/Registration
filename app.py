import flask
import requests
from flask import Flask, render_template, request, redirect
import psycopg2

alphabet = 'qwertyuiopasdfghjklzxcvbnm1234567890()!@#$%*{}[]|\?/`_-+=.'

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="123",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            a = [check(username, 0), check(password, 0)]
            if a.count('good') != 2:
                return render_template('login.html', attention=a[0] if a[0] != 'good' else a[1])
            else:
                cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s",
                               (str(username), str(password)))
                records = list(cursor.fetchall())
                return render_template('account.html', full_name=records[0][1])
        elif request.form.get("registration"):
            return redirect("/registration/")

    return render_template('login.html')


@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')

        list_ = [name, login, password]
        for i, line in enumerate(list_):
            list_[i] = check(line, i)
            if list_[i] != 'good':
                return render_template('registration.html', attention=list_[i])
        if list_.count('good') == 3:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password)))
            conn.commit()

            return redirect('/login/')

    return render_template('registration.html')


def check(line, num):
    if num == 1:
        cursor.execute("SELECT login FROM service.users WHERE login=%s",
                       (str(line),))
        records = list(cursor.fetchall())
        if len(records) != 0:
            return 'Такой логин уже занят'
    if len(line) == 0:
        return 'Одна или несколько строк ничего не содержат'
    elif len(line) <= 2:
        return 'Одна или несколько строк слишком короткие, минимальная длина 3'
    elif line.count(' ') != 0:
        return 'Одна или несколько строк имеют пробелы'
    else:
        for s in line.lower():
            if s not in alphabet:
                return 'Одна или несколько строк имеют запрешённые символы'
        return 'good'


if __name__ == '__main__':
    app.run()
