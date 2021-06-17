# Python Recruitment Control System

Project Name: Recruitment Control System

Used Technologies: Python Flask, MSSQL server, PyCharm, HTML, Basic Bootstrap,

The aim of this project is to to combine employers with job applicants in a system. 
Job Applicants enter their resume information and the position they want to apply. 
While employers enter the positions (open vacancies) they open for applicants.
For now the insert, update, delete and get methods are developed and with basic html files are used.

In the Version 2 I developed a function for the Employers such that there is an email sending button "publishedCandidates". 
In the RecruitmentCSManagement.py publishedCandidates function running to send emails for the suitable Applicants.
There are conditions" both for Employers and Applicants to be suitable to each other. 
And these are; "item_candidate.position == my_data_employer.position 
and item_candidate.city == my_data_employer.city 
and item_candidate.is_active. 
In the Version 3 there is a general chart for Sent Mails and Positions columns in the Home page.

In this web project Python Flask and MSSQL server is used.

#SqlAlchemy Database Configuration With MSSQL server
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://username:psw@servername/DBname?driver=SQL+Server'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

pip install Flask
pip install Flask-SQLAlchemy
pip install pyodbc
pip install Flask-Mail
