import json
import random
import time
import smtplib
import sys
from flask_mail import Mail, Message
from datetime import datetime

from flask import Flask, render_template, request, redirect, url_for, flash, Response
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)

mail = Mail(app) #SECOND WAY

app.secret_key = "Secret Key"

#added for emails.
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'example@gmail.com'
app.config['MAIL_PASSWORD'] = 'example'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
mail = Mail(app)


#SqlAlchemy Database Configuration With mssql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://username:examplepws@Server/DataBase?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


#Creating Model
class Mail_history(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    candidate_email = db.Column(db.String(100))
    position = db.Column(db.String(100))
    city = db.Column(db.String(100))
    company = db.Column(db.String(150))
    sent_date = db.Column(db.DateTime)


    def __init__(self, candidate_email, position, city, company, sent_date):

        self.candidate_email = candidate_email
        self.position = position
        self.city = city
        self.company = company
        self.sent_date = sent_date


#Creating model
class Employer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    company = db.Column(db.String(150))
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

    #is_active = db.Column(db.Boolean, unique=False)


    def __init__(self, name, surname, company, position, city, email, phone, description, create_date, edit_date, is_active, published_date, is_published):

        self.name = name
        self.surname = surname
        self.company = company
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


#Creating model
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


@app.route('/mailhistory')
def Mail_History():
    all_mail_history = Mail_history.query.all()

    return render_template("mail_history.html", mail_history = all_mail_history)


@app.route('/')
def Index():

    mail_history_list = Mail_history.query.all()
    labels = [] #["01-01-2020", "02-01-2020","03-01-2020","04-01-2020","05-01-2020"]
    values = [] #[123,443,55676,7543,3543]
    for item_mail_history in mail_history_list:
        labels.append(item_mail_history.sent_date)
        values.append(item_mail_history.id)

    return render_template("index.html", labels = labels, values = values)


@app.route('/candidates')
def candidates():
    all_Candidate = Candidate.query.all()

    return render_template('candidates.html', candidates = all_Candidate)


@app.route('/employers')
def employers():
    all_Employer = Employer.query.all()

    return render_template('employers.html', employers = all_Employer)


def insertMailHistory(item_candidate, company, published_date):
    candidate_email = item_candidate.email
    position = item_candidate.position
    city = item_candidate.city
    company = company
    sent_date = published_date

    my_data = Mail_history(candidate_email, position, city, company, sent_date)
    db.session.add(my_data)
    db.session.commit()


#This route is for deleting our employers
@app.route('/deleteMailHistory/<id>/', methods = ['GET', 'POST'])
def deleteMailHistory(id):
    my_data = Mail_history.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Mail History Row Deleted Successfully")

    return redirect(url_for('Mail_History'))


def mailsender(candidate_email, is_mail_sent, my_data_employer):
    try:
        msg = Message('Hello', sender='diner.metu@gmail.com', recipients=[candidate_email])
        msg.body = "We are happy to inform that you are suitable for the position: " + my_data_employer.position + " in the " + my_data_employer.company + " company" + " in the city of " + my_data_employer.city

        mail.send(msg)
        is_mail_sent = True
        return is_mail_sent
    except Exception as e:
        is_mail_sent = False
        flash("Error: " + str(e))
        return is_mail_sent


@app.route('/publishedCandidates/<id>/', methods = ['GET', 'POST'])
def publishedCandidates(id):
    my_data_employer = Employer.query.get(id)
    my_data_candidate_list = Candidate.query.all()
    is_mail_sent = False

    if my_data_employer.id != 0 and my_data_employer.is_active is True: #if my_data_employer is not empty
        for item_candidate in my_data_candidate_list:
            is_mail_sent = False
            # if belove conditions are True
            if item_candidate.position == my_data_employer.position and item_candidate.city == my_data_employer.city and item_candidate.is_active is True:
                # if mailsender function's return is True, mailsender function takes 3 parameter; (email,is_mail_sent, my_data_employer)
                if mailsender(item_candidate.email, is_mail_sent, my_data_employer) is True: # mailsender function
                    my_data_employer.is_published = True
                    my_data_employer.published_date = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
                    # insertMailHistory called
                    insertMailHistory(item_candidate, my_data_employer.company, my_data_employer.published_date)
                    db.session.commit()

        flash("Published Successfully")

    return redirect(url_for('employers'))


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
            my_data.is_active = False

        db.session.commit()
        flash("Candidate Updated Successfully")

        return redirect(url_for('candidates'))


@app.route('/deleteCandidates/<id>/', methods = ['GET', 'POST'])
def deleteCandidates(id):
    my_data = Candidate.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Candidate Deleted Successfully")

    return redirect(url_for('candidates'))


@app.route('/insertEmployers', methods = ['POST'])
def insertEmployers():

    if request.method == 'POST':

        name = request.form['name']
        surname = request.form['surname']
        company = request.form['company']
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

        my_data = Employer(name, surname, company, position, city, email, phone, description, create_date, edit_date, is_active, published_date, is_published)
        db.session.add(my_data)
        db.session.commit()

        flash("Employer Inserted Successfully")

        return redirect(url_for('employers'))


@app.route('/updateEmployers', methods = ['GET', 'POST'])
def updateEmployers():

    if request.method == 'POST':
        my_data = Employer.query.get(request.form.get('id'))

        my_data.name = request.form['name']
        my_data.surname = request.form['surname']
        my_data.company = request.form['company']
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


#This route is for deleting our employers
@app.route('/deleteEmployers/<id>/', methods = ['GET', 'POST'])
def deleteEmployers(id):
    my_data = Employer.query.get(id)
    db.session.delete(my_data)
    db.session.commit()
    flash("Employer Deleted Successfully")

    return redirect(url_for('employers'))


if __name__ == "__main__":
    app.run(debug=True)
