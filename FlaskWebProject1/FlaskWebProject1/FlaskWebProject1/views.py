"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import Flask, render_template
from FlaskWebProject1 import app
import pyodbc
from datetime import datetime    
    
from flask import render_template, redirect, request 

conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=LAPTOP-67SG5599;'
                      'Database=consumerdb;'
                      'Trusted_Connection=yes;')
cursor = conn.cursor()
cursor.execute('SELECT * FROM consumerdb.dbo.def')

for row in cursor:
    print(row)

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )

@app.route('/contact')
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Contact',
        year=datetime.now().year,
        message='Your contact page.'
    )

@app.route('/about')
def about():
    """Renders the about page."""
    return render_template(
        'about.html',
        title='About',
        year=datetime.now().year,
        message='Your application description page.'
    )
