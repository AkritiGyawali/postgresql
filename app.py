from flask import Flask,render_template,redirect,url_for,flash,request ,session,jsonify
import psycopg2
from psycopg2 import pool
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

# Database connection function using Neon connection string
def get_db_connection():
    DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://neondb_owner:npg_mIq6DnStlPT0@ep-raspy-flower-a1ddrzcr-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require')
    max_retries = 3
    for attempt in range(max_retries):
        try:
            conn = psycopg2.connect(DATABASE_URL)
            # Test the connection
            cursor = conn.cursor()
            cursor.execute('SELECT 1')
            cursor.close()
            return conn
        except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
            print(f"Connection attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e

# Initialize database connection when needed
mydb = None
mycursor = None

# Disable connection pool for now - use direct connections
db_pool = None
def init_db():
    global mydb, mycursor
    try:
        # Always create a fresh connection to avoid stale connections
        if mydb is not None:
            try:
                mydb.close()
            except:
                pass
        
        mydb = get_db_connection()
        mycursor = mydb.cursor()
        print("✅ Database connection established")
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        mydb = None
        mycursor = None
        raise e

app.config['DB_config'] = mydb
app.register_blueprint(home_bp)

bcrypt=Bcrypt(app)
app.config['SECRET_KEY']=os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(username):
    init_db()
    mycursor.execute('SELECT * FROM "user" WHERE username=%s', (username,))
    user_data=mycursor.fetchone()
    if user_data:
        return User(user_data[3], user_data[3], user_data[4])  # id, username, password
    return None



class registerform(FlaskForm):# register form inherits from FlaskForm
    FirstName=StringField(validators=[InputRequired()],render_kw={"placeholder":"First Name"})
    LastName=StringField(validators=[InputRequired()],render_kw={"placeholder":"Last Name"})
    username=StringField(validators=[InputRequired(),Length(min=4,max=15)],render_kw={"placeholder":"Username"})# username is the form field and username.data is the actual data entered by the user in the form
    email=EmailField(validators=[InputRequired(),Email()],render_kw={"placeholder":"Email"})# email is the form field and email.data is the actual data entered by the user in the form
    password=PasswordField(validators=[InputRequired(),Length(min=8,max=20)],render_kw={"placeholder":"Password"})# password is the form field and password.data is the actual data entered by the user in the form
    
    confirm_password=PasswordField(validators=[InputRequired(),Length(min=8,max=20),EqualTo('password',message='password must match')],render_kw={"placeholder":"confrim-password"})
    
    submit=SubmitField('Send Otp')

    def validate_username(self,username):
        init_db()
        mycursor.execute('SELECT * FROM "user" WHERE username=%s',(username.data,))
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
    if form.validate_on_submit():
        init_db()
        mycursor.execute('SELECT * FROM "user" WHERE username=%s',(form.username.data,))
        user_data=mycursor.fetchone()
        if user_data:
            # Use plain text password comparison (password is at index 3)
            if user_data[4] == form.password.data:
                user = User(user_data[3], user_data[3], user_data[4])  # id, username, password
                login_user(user)
                return redirect(url_for('home.home'))
            else:
                print(f"Form password: {form.password.data}")
                print(f"DB password: {user_data[4]}")
                flash("Invalid password",'danger')
                return redirect('/')
        else:
          flash("It seems you don't have an account. Please register!!", 'danger')
          return redirect('/')
    return render_template('login.html',form=form)# here we pass the form to the html



@app.route('/register',methods=['POST','GET'])
def register():
        
    form=registerform()
    print('form created')
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        firstname = form.FirstName.data
        lastname = form.LastName.data
        passwd = form.password.data  # Use plain text password for testing
        # Remove hashed password for plain text testing
        
        global cred 
        cred = {'email':email,'username':username,'hash_pass': passwd,'firstname':firstname,'lastname':lastname}
        generate_and_send_otp(email)
        
        flash('otp has been send to your email . Please verify to register', 'success')
        time.sleep(4)
        return redirect(url_for('otp'))
    return render_template('register.html',form=form)# here we pass the register form to the template

@app.route('/otp', methods=['GET','POST'])
def otp():
    otpp=otpform()
    email = cred.get('email')
    username = cred.get('username')
    password = cred.get('hash_pass')
    firstname = cred.get('firstname')
    lastname = cred.get('lastname')
    if request.method == 'POST':
        code = request.form['otp']
        otp_code = otp_store.get(email)['otp']
        if code == otp_code:
            init_db()
            mycursor.execute('INSERT INTO "user" (first_name,last_name,username,password,email) VALUES (%s,%s,%s,%s,%s)',(firstname,lastname,username,password,email))
            mydb.commit()
            
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


@app.route("/users")
def get_users():
    try:
        init_db()
        mycursor.execute('SELECT username FROM "user"')
        rows = mycursor.fetchall()
        return jsonify([row[0] for row in rows])  # Return just usernames as list
    except Exception as e:
        print(f"Error in /users route: {e}")
        return {"error": str(e)}, 500





if __name__=='__main__':
    app.run(debug =True,host='0.0.0.0',port='8080')
