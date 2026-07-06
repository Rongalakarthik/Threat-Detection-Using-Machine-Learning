from flask import Flask,url_for,redirect,render_template,request,session
import mysql.connector
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np
import joblib

app  = Flask(__name__)
app.secret_key = 'admin'




@app.route('/')
def index():
    return render_template('index.html')



@app.route('/about')
def about():
    return render_template('about.html')

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return



mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    port="3306",
    database='network'
)

mycursor = mydb.cursor()

def executionquery(query,values):
    mycursor.execute(query,values)
    mydb.commit()
    return

def retrivequery1(query,values):
    mycursor.execute(query,values)
    data = mycursor.fetchall()
    return data

def retrivequery2(query):
    mycursor.execute(query)
    data = mycursor.fetchall()
    return data

# @app.route('/register' ,methods = ['GET',"POST"])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         phone = request.form['phone']
#         email = request.form['email']
#         password = request.form['password']
#         c_password = request.form['c_password']
#         if password == c_password:
#             query = "SELECT email FROM users"
#             email_data = retrivequery2(query)
#             email_data_list = []
#             for i in email_data:
#                 email_data_list.append(i[0])
#                 if email not in email_data_list:
#                     query = "INSERT INTO users (name,email, password,phone) VALUES ( %s, %s, %s,%s)"
#                     values = (name,email, password,phone)
#                     executionquery(query, values)
#                     return render_template('login.html', message="Successfully Registered!")
#                 return render_template('register.html', message="Enter the valid inputs...!")
#         return render_template('register.html', message="Conform password is not match!")
#     return render_template('register.html')
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']
        c_password = request.form['c_password']
        
        # Check if passwords match
        if password != c_password:
            return render_template('register.html', message="Confirm password does not match!")
        
        # Retrieve existing emails
        query = "SELECT email FROM users"
        email_data = retrivequery2(query)
        
        # Create a list of existing emails
        email_data_list = [i[0] for i in email_data]
        
        # Check if the email already exists
        if email in email_data_list:
            return render_template('register.html', message="Email already exists!")

        # Insert new user into the database
        query = "INSERT INTO users (name, email, password, phone) VALUES (%s, %s, %s, %s)"
        values = (name, email, password, phone)
        executionquery(query, values)
        
        return render_template('login.html', message="Successfully Registered!")
    
    return render_template('register.html')



@app.route('/login',methods = ["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']

        query = "SELECT email FROM users"
        email_data = retrivequery2(query)
        email_data_list = []
        for i in email_data:
            email_data_list.append(i[0])

        if email in email_data_list:
            query = "SELECT name, password FROM users WHERE email = %s"
            values = (email, )
            password__data = retrivequery1(query, values)
            if password == password__data[0][1]:
                global user_email
                user_email = email

                name = password__data[0][0]
                session['name'] = name
                print(f"User name: {name}")
                return render_template('home.html',message= f"Welcome to Home page {name}")
            return render_template('login.html', message= "Invalid Password!!")
        return render_template('login.html', message= "This email ID does not exist!")
    return render_template('login.html')
    

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/upload', methods=["GET", "POST"])
def upload():
    if request.method == "POST":
        file = request.files['file']
        df = pd.read_csv(file, encoding='latin1') 
        df = df.to_html()
        return render_template('upload.html', df=df)
    return render_template('upload.html')

@app.route('/info')
def info():
    return render_template('data_info.html')


@app.route('/model',methods =["GET","POST"])
def model():
    if request.method == "POST":
        algorithams = request.form["algo"]
        if algorithams == "0":
            msg = 'select the Algoritham'
            return render_template('model.html',msg=msg)
        elif algorithams == "1":
            accuracy = 99
            msg = 'Accuracy  for Decision tree  is ' + str(accuracy) + str('%')
        elif algorithams == "2":
            accuracy = 99
            msg = 'Accuracy  for Random_Forest Classifier is ' + str(accuracy) + str('%')
        elif algorithams == "3":
            accuracy = 76
            msg = 'Accuracy  for SVC  is ' + str(accuracy) + str('%')
        elif algorithams == "4":
            accuracy = 99
            msg = 'Accuracy  for Extra Tree Classifier is ' + str(accuracy) + str('%')
        elif algorithams == "5":
            accuracy = 91
            msg = 'Accuracy  for KNN Classifier is ' + str(accuracy) + str('%')
        elif algorithams == "6":
            accuracy = 60
            msg = 'Accuracy  for Deep Nural Network is ' + str(accuracy) + str('%')

        
        return render_template('model.html',msg=msg,accuracy = accuracy)
    return render_template('model.html')




@app.route('/prediction', methods=["GET", "POST"])
def prediction():
 
    return render_template('prediction.html')
     

    

    
    



if __name__ == '__main__':
    app.run(debug=True)