#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Assignemnt Week 13 - Flask App"""

from flask import Flask, render_template, request, redirect, session, url_for
import re
app = Flask(__name__)
app.secret_key = 'lasso91'

@app.route('/')
def index():
    print session
    return render_template('index.html')

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
                return redirect('/Dashboard')
            else:
                session['Logged_In'] = 'N'
                error = 'Incorrect login or password'
                return render_template('Login.html', error=error)
        else:
            return render_template('Login.html')
    else:
        #validate Sessions Info
        #return render_template('login.html', error=error)
        return redirect('/Dashboard')

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('User_Id', None)
    session.pop('Logged_In', None)
    return redirect(url_for('index'))

"""
@app.route('/submit', methods = ['POST'])


@app.route('/clear', methods = ['POST'])
"""

if __name__ == '__main__':
    app.run()