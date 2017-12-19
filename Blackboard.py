#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignemnt Week 13 - Flask App"""

from flask import Flask, render_template, request, redirect, session, url_for
import re
import sqlite3 as lite

con = lite.connect('hw13.db')
con.row_factory = lite.Row
cursor = con.cursor()

def init_db():
    with open('schema.sql') as db:
        cursor.executescript(db.read())

    temp_student = (301101,'John', 'Smith')
    temp_quiz = (201, 'Python Basics', 5, '02-05-2015')
    temp_grade = (1, 301101, 201, 85)

    cursor.execute('INSERT into student(Identifier, FirstName, LastName) VALUES (?,?,?)', temp_student)
    cursor.execute('INSERT into quizzes(Identifier, Subject,TotalQuestions, Date) VALUES (?,?,?,?)', temp_quiz)
    cursor.execute('INSERT into grades(Identifier, Student, Quiz, Grade) VALUES (?,?,?)', temp_grade)

app = Flask(__name__)
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

    if valid:
        return render_template('dashboard.html')
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