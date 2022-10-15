import random
from twilio.rest import *
from flask import *
from pymongo import MongoClient
a = MongoClient('mongodb://127.0.0.1:27017')
db = a['Website']
customer =db.customer
app=Flask(__name__)
app.secret_key='otp'
#REDIRECT TO HOME PAGE
@app.route('/')
def homepage():
    return render_template('homepage.html')
@app.route('/menu')
def menu():
    return render_template('delivery.html')
@app.route('/breakfast')
def breakfast():
    return render_template('breakfast.html')
#REDIRECT TO LOGIN PAGE
@app.route('/Login')
def loginpage():
    return render_template('login.html')
#LOGIN DETAILS VERIFICATION
@app.route('/Login/Submit',methods=['GET', 'POST'])
def verification_login_details():
    if request.method == 'POST':
        vid = customer.find_one({'email':request.form["email"]})
        vpsw = customer.find_one({'Password':request.form["pass"]})
        if vid is None and vpsw is None:
            return 'You are not registered please register and login'
        elif vid is not None and vpsw is None:
            return 'WRONG PASSWORD'
        else:
            return 'success  fully login'
#REDIRECT TO REGISTER PAGE
@app.route('/Register', methods=['GET', 'POST'])
def registerpage():
    return render_template('register.html')
#REGISTER DETAILS STORING IN DATABASE
@app.route('/getotp',methods=['GET', 'POST'])
def getotp():
    if request.method == 'POST':
        exesting_user=customer.find_one({'email':request.form["email"]})
    if exesting_user is None:
        fname=request.form.get("firstname")
        lname=request.form.get("lastname")
        email=request.form.get("email")
        mbl=request.form.get("mobilenumber")
        password=request.form.get("psw")
        a={"First name":fname,"Last name":lname,"Email":email,"Mobile Number":mbl,"Password":password}
        customer.insert_one(a)
        number = request.form.get("mobilenumber")
        val=getotpapi(number)
        if val:
            return render_template('otpverification.html',fname=fname,mbl=mbl)
    else:
        return 'email id is already used'
@app.route('/validateotp',methods=['GET', 'POST'])
def validateotp():
    otp=request.form['otp']
    if 'response' in session:
        s=session['response']
        session.pop('response',None)
        if s == otp:
            return 'correct'
        else:
            return 'incorrect'
def generateOTP():
    return random.randrange(100000,999999)
def getotpapi(number):
    account_sid='AC3e6429dc67e942f7df3944977492d00f'
    auth_token='545ee9af4d8ec55b010a275839079a47'
    client = Client(account_sid,auth_token)
    otp=generateOTP()
    session['response']=str(otp)
    body ='Your OTP is'+str(otp)
    message = client.messages.create(
    from_='+13854858851',
    body=body,
    to=number)
    if message.sid:
        return True
    else:
        False
if __name__ == '__main__':
    app.run()