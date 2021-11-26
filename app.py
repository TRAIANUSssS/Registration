import flask
import requests
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="123",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/login/', methods=['POST', 'GET'])
def login():
    attention = 'Введите корректное значение'

    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            if (username == '') or (username.count(' ') != 0) or (password.count(' ') != 0) or (password == ''):
                return render_template('login.html', attention='Введите некорректные данные')
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
        if (login == '') or (login.count(' ') != 0) or (password.count(' ') != 0) or (password == '') or (
                name == '') or (name.count(' ') > 3) or (len(name) == name.count(' ')):
            return render_template('registration.html', attention='Введите некорректные данные')
        else:
            cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);',
                           (str(name), str(login), str(password)))
            conn.commit()

            return redirect('/login/')

    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
