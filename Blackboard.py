#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignemnt Week 13 - Flask App"""

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import re
import sqlite3 as lite
from contextlib import closing

DATABASE = 'hw13.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'password'

app = Flask(__name__)
app.config.from_object(__name__)

con = lite.connect('hw13.db')

cur = con.cursor()

cur.executescript("""
    DROP TABLE IF EXISTS student;
    DROP TABLE IF EXISTS quizzes;
    DROP TABLE IF EXISTS grades;
    CREATE TABLE student(Identifier INTEGER PRIMARY KEY, FirstName TEXT, LastName TEXT);
    CREATE TABLE quizzes(Identifier INTEGER PRIMARY KEY, Subject TEXT, TotalQuestions INTEGER, Date TEXT);
    CREATE TABLE grades(Identifier INTEGER PRIMARY KEY, Student INTEGER, Quiz INTEGER, Grade INTEGER, FOREIGN KEY (Student) REFERENCES student(Identifier), FOREIGN KEY (Quiz) REFERENCES quizzes(Identifier));
    """)

cur.execute('INSERT into student VALUES (1201,"John","Smith");')
cur.execute('INSERT into quizzes VALUES (101,"Python Basics",5,"12-05-2015");')
cur.execute('INSERT into grades VALUES (1,1201,101,85);')

cur.execute('INSERT into student VALUES (1202,"Rommel","Lasso");')
cur.execute('INSERT into grades VALUES (2,1202,101,100);')

con.commit()

def connect_db():
    return lite.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

#app = Flask(__name__)
app.secret_key = 'lasso91'

def getSessionInfo ():
    token = ''
    if session['User_Id']>0:
        token = True
    return token

@app.route('/')
def index():
    print session
    return render_template('index.html')

@app.route('/dashboard')
def deashboard():
    valid = getSessionInfo()

    student_data = {}

    conns = g.db.execute('select Identifier, FirstName, LastName from student')
    students = [dict(StudentID=row[0], FirstName=row[1], LastName=row[2])
               for row in conns.fetchall()]

    conns = g.db.execute('select Identifier, Subject, TotalQuestions, Date from quizzes')
    quizzes = [dict(QuizId=row[0], Subject=row[1], TotalQuestions=row[2], Date=row[3])
                for row in conns.fetchall()]

    if valid:
        return render_template('dashboard.html', students = students, quizzes = quizzes)
    else:
        return redirect(url_for('index'))


@app.route('/login', methods=['GET','POST'])
def login():
    error = None

    print 'entering login'

    # Check if we alredy have sessionInfo
    if len(session) == 0 or session['Logged_In']=='N':
        if request.method == 'POST':
            print 'entering login POST'
            if request.form['email'] == 'admin' and request.form['password'] == 'password':
                session['Logged_In'] = 'Y'
                session['User_Id'] = 1
                return redirect("/dashboard")
            else:
                session['Logged_In'] = 'N'
                error = 'Incorrect login or password'
                return render_template('Login.html', error=error)
        else:
            return render_template('Login.html')
    else:
        #validate Sessions Info
        #return render_template('login.html', error=error)
        return redirect('/dashboard')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('User_Id', None)
    session.pop('Logged_In', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()