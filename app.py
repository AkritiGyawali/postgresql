from flask import Flask,render_template,redirect,url_for,flash,request ,session
import mysql.connector
from mysql.connector import Error
from flask_login import UserMixin,login_user,LoginManager,login_required,logout_user,current_user
from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.fields import EmailField
from wtforms.validators import InputRequired,Length,Email,ValidationError,EqualTo
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
import random
import time
from datetime import datetime,timedelta
from home import home_bp
import os
from dotenv import load_dotenv
load_dotenv()


app= Flask(__name__)
app.register_blueprint(home_bp)

sqhost=os.getenv('host')
squser=os.getenv('username')
sqpassword=os.getenv('password')
sqdatabase=os.getenv('database')
app.config['SESSION_TYPE']='filesystem'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = os.getenv('User_id')
app.config['MAIL_PASSWORD'] = os.getenv('Pass_key')

app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)
otp_store = {}
cred = {}
mydb=mysql.connector.connect(

    host=sqhost,
    user=squser,
    password=sqpassword,
    database=sqdatabase
)

mycursor=mydb.cursor()

bcrypt=Bcrypt(app)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    mycursor.execute('SELECT * FROM user WHERE username=%s', (username,))
    user_data=mycursor.fetchone()
    if user_data:
        return User( user_data[0],user_data[0], user_data[1])  # Assuming user_id is the first column in the user table
    return None







                          



 

class registerform(FlaskForm):# register form inherits from FlaskForm
    FirstName=StringField(validators=[InputRequired()],render_kw={"placeholder":"First Name"})
    LastName=StringField(validators=[InputRequired()],render_kw={"placeholder":"Last Name"})
    username=StringField(validators=[InputRequired(),Length(min=4,max=15)],render_kw={"placeholder":"Username"})# username is the form field and username.data is the actual data entered by the user in the form
    email=EmailField(validators=[InputRequired(),Email()],render_kw={"placeholder":"Email"})# email is the form field and email.data is the actual data entered by the user in the form
    password=PasswordField(validators=[InputRequired(),Length(min=8,max=20)],render_kw={"placeholder":"Password"})# password is the form field and password.data is the actual data entered by the user in the form
    
    confirm_password=PasswordField(validators=[InputRequired(),Length(min=8,max=20),EqualTo('password',message='password must match')],render_kw={"placeholder":"confrim-password"})
    #abc = StringField(validators=[InputRequired()],render_kw={"placeholder":"Enter OTP"})# abc is the form field and abc.data is the actual data entered by the user in the form
    
    submit=SubmitField('Send Otp')

    def validate_username(self,username):
        mycursor.execute('SELECT * FROM user WHERE username=%s',(username.data,))
        user=mycursor.fetchone()
        if user:
            raise ValidationError('username already exists,please choose a different one')

class otpform(FlaskForm):
    otp=StringField(validators=[InputRequired()],render_kw={"placeholder":"Enter OTP"})    
    submit=SubmitField('Register')



class loginform(FlaskForm):#loginform inherits from flaskform
    username=StringField(validators=[InputRequired(),Length(min=4,max=15)],render_kw={'placeholder':"Username"})# username is the form field and username.data is the actual data entered by the user in the form
    password=PasswordField(validators=[InputRequired(),Length(min=8,max=20)],render_kw={'placeholder':"Password"})# password is the form field and password.data is the actual data entered by the user in the form
    submit=SubmitField('Login')


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = username
        self.username = username
        self.password = password

def generate_and_send_otp(email):
    otp = str(random.randint(100000, 999999))
    print(otp)
    
    otp_store[email] = {
        'otp': otp,
        'expires_at': datetime.utcnow() + timedelta(minutes=5)
    }
    msg = Message('Your Login OTP Code', sender=app.config['MAIL_USERNAME'], recipients=[email])
    msg.body = f'Your OTP is: {otp}. It will expire in 5 minutes.'
    mail.send(msg)


@app.route('/',methods=['POST','GET'])
def login():
    form=loginform()
    if form.validate_on_submit():# class form ko requirement pura vhayo vaney
        mycursor.execute('SELECT * FROM user WHERE username=%s',(form.username.data,))# yeslay user ley login form ma enter gareyko username database me store xa kinai vaneyrw check garxa
        user_data=mycursor.fetchone()
        if user_data:
            
            user = User( user_data[0],user_data[0], user_data[1])  # Assuming user_id is the first column in the user table
            if bcrypt.check_password_hash(user.password,form.password.data):
                # user_id is the first column in the user table
                login_user(user)
            
                return redirect(url_for('home.home'))# login_user function from flask_login module is used to log in the user
            else:
                flash("password elayy",'danger')
                return redirect('/')
        else:
          flash("It seems you don't have an account. Please register!!", 'danger')
          return redirect('/')
    return render_template('login.html',form=form)# here we pass the form to the html


# @app.route('/home',methods=['POST','GET'])
# @login_required
# def home():
#     return render_template('home.html')

@app.route('/register',methods=['POST','GET'])
def register():
        
    form=registerform()
    print('form created')
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        firstname = form.FirstName.data
        lastname = form.LastName.data
        hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        global cred 
        cred = {'email':email,'username':username,'hash_pass': hashed_password,'firstname':firstname,'lastname':lastname}
        print(f'email direct {email}')
        print(f'email stored {cred.get('email')}')
        generate_and_send_otp(email)
        print('otp sent')
        # Registration logic here
        # mycursor.execute("INSERT INTO users (username,email,is_verified) VALUES (%s,%s,%s)", (username, email, False))
        # mydb.commit()
        flash('otp has been send to your email . Please verify to register', 'success')
        time.sleep(4)
        print('error 1')
        return redirect(url_for('otp'))
    print('error 2')
    return render_template('register.html',form=form)# here we pass the register form to the template

@app.route('/otp', methods=['GET','POST'])
def otp():
    otpp=otpform()
    email = cred.get('email')
    username = cred.get('username')
    password = cred.get('hash_pass')
    firstname = cred.get('firstname')
    lastname = cred.get('lastname')
    print(email)
    if request.method == 'POST':
        code = request.form['otp']
        print(f'email inside {email}')
        otp_code = otp_store.get(email)['otp']
        print(f'otp code list{otp_code}')
        if code == otp_code:
            mycursor.execute("INSERT INTO user (first_name,last_name,username,password,email) VALUES (%s,%s,%s,%s,%s)",(firstname,lastname,username,password,email))
            mydb.commit()
            print("otp verified")
            return redirect('/')
        else:
            print('otp not verified')
            flash('otp error')
            return redirect('/otp')
    
    return render_template('otp.html',otpp=otpp)

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__=='__main__':



    app.run(debug =True)
