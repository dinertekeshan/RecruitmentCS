import json
import random
import time
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.secret_key = "Secret Key"

#SqlAlchemy Database Configuration With Mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://sa:C1086134@DESKTOP-81V57KU/RecruitmentCS?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating model table for our CRUD database
class Employer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    position = db.Column(db.String(100))
    city = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    description = db.Column(db.String(100))
    create_date = db.Column(db.DateTime)
    edit_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    published_date = db.Column(db.DateTime)
    is_published = db.Column(db.Boolean, default=False)


    def __init__(self, name, surname, position, city, email, phone, description, create_date, edit_date, is_active, published_date, is_published):

        self.name = name
        self.surname = surname
        self.position = position
        self.city = city
        self.email = email
        self.phone = phone
        self.description = description
        self.create_date = create_date
        self.edit_date = edit_date
        self.is_active = is_active
        self.published_date = published_date
        self.is_published = is_published


#Creating model table for our CRUD database
class Candidate(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    TCNo = db.Column(db.String(11))
    position = db.Column(db.String(100))
    city = db.Column(db.String(100))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(100))
    description = db.Column(db.String(100))
    create_date = db.Column(db.DateTime)
    edit_date = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)

    #is_active = db.Column(db.Boolean, unique=False)


    def __init__(self, name, surname, TCNo, position, city, email, phone, description, create_date, edit_date, is_active):

        self.name = name
        self.surname = surname
        self.TCNo = TCNo
        self.position = position
        self.city = city
        self.email = email
        self.phone = phone
        self.description = description
        self.create_date = create_date
        self.edit_date = edit_date
        self.is_active = is_active



#This is the index route where we are going to
#query on all our employee data
@app.route('/')
def Index():
    all_Candidate = Candidate.query.all()
    all_Employer = Employer.query.all()

    return render_template("index.html")



@app.route('/candidates')
def candidates():
    all_Candidate = Candidate.query.all()

    return render_template('candidates.html', candidates = all_Candidate)


@app.route('/employers')
def employers():
    all_Employer = Employer.query.all()

    return render_template('employers.html', employers = all_Employer)


#this route is for inserting data to mysql database via html forms
@app.route('/insertCandidates', methods = ['POST'])
def insertCandidates():

    if request.method == 'POST':

        name = request.form['name']
        surname = request.form['surname']
        TCNo = request.form['TCNo']
        position = request.form['position']
        city = request.form['city']
        email = request.form['email']
        phone = request.form['phone']
        description = request.form['description']
        create_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        edit_date = None
        is_active = False
        if request.form.get("is_active"):
            is_active = True

        my_data = Candidate(name, surname, TCNo, position, city, email, phone, description, create_date, edit_date, is_active)
        db.session.add(my_data)
        db.session.commit()

        flash("Candidate Inserted Successfully")

        return redirect(url_for('candidates'))


#this is our update route where we are going to update our employee
@app.route('/updateCandidates', methods = ['GET', 'POST'])
def updateCandidates():

    if request.method == 'POST':
        my_data = Candidate.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.surname = request.form['surname']
        my_data.TCNo = request.form['TCNo']
        my_data.position = request.form['position']
        my_data.city = request.form['city']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.description = request.form['description']
        my_data.edit_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        if request.form.get("is_active"):
            my_data.is_active = True
        else:
            my_data.is_active=False

        db.session.commit()
        flash("Candidate Updated Successfully")

        return redirect(url_for('candidates'))




#This route is for deleting our employee
@app.route('/deleteCandidates/<id>/', methods = ['GET', 'POST'])
def deleteCandidates(id):
    my_data = Candidate.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Candidate Deleted Successfully")

    return redirect(url_for('candidates'))


#this route is for inserting data to mysql database via html forms
@app.route('/insertEmployers', methods = ['POST'])
def insertEmployers():

    if request.method == 'POST':

        name = request.form['name']
        surname = request.form['surname']
        position = request.form['position']
        city = request.form['city']
        email = request.form['email']
        phone = request.form['phone']
        description = request.form['description']
        create_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        edit_date = None #(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        is_active = False
        if request.form.get("is_active"):
            is_active = True
        published_date = None #(datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        is_published = False

        my_data = Employer(name, surname, position, city, email, phone, description, create_date, edit_date, is_active, published_date, is_published)
        db.session.add(my_data)
        db.session.commit()

        flash("Employer Inserted Successfully")

        return redirect(url_for('employers'))


#this is our update route where we are going to update our employee
@app.route('/updateEmployers', methods = ['GET', 'POST'])
def updateEmployers():

    if request.method == 'POST':
        my_data = Employer.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.surname = request.form['surname']
        my_data.position = request.form['position']
        my_data.city = request.form['city']
        my_data.email = request.form['email']
        my_data.phone = request.form['phone']
        my_data.description = request.form['description']
        my_data.edit_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
        if request.form.get("is_active"):
            my_data.is_active = True
        else:
            my_data.is_active = False

        db.session.commit()
        flash("Employer Updated Successfully")

        return redirect(url_for('employers'))


#This route is for deleting our employee
@app.route('/deleteEmployers/<id>/', methods = ['GET', 'POST'])
def deleteEmployers(id):
    my_data = Employer.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employer Deleted Successfully")

    return redirect(url_for('employers'))


if __name__ == "__main__":
    app.run(debug=True)