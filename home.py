from flask import Blueprint, render_template,request,redirect , flash,url_for, request
from flask_login import login_required,current_user

import psycopg2
import httpx
import os
import time
from dotenv import load_dotenv
load_dotenv()


stock_list= {}
api_url = 'https://nepalstock.onrender.com/securityDailyTradeStat/58'
home_bp= Blueprint('home', __name__) 

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

@home_bp.route('/home',methods=['POST','GET'])
@login_required
def home():
    init_db()  # Always refresh connection
 
    if request.method=='POST':
        stock_name=request.form['stock_name']
        req = httpx.get (api_url,timeout=15)
        if req.status_code == 200:
            data = req.json()
            for item in data:
                found = False
                if item["symbol"] == stock_name.upper():
                    stock_naam = item['symbol']
                    stock_id = item['securityId']
                    ltp = item['lastTradedPrice']
                    stock_list = {
                        'name': stock_naam,
                        'id': stock_id,
                        'ltp': ltp
                    }
                    init_db()  # Refresh connection before insert
                    mycursor.execute("INSERT INTO showw(stock_name,stock_id,ltp,username)VALUES(%s,%s,%s,%s)",(stock_list['name'],stock_list['id'],stock_list['ltp'],current_user.username))
                    mydb.commit()
                    found = True
                    break
                
                   

            if not found:
                flash(f"Invalid stock name", 'danger')
                return redirect('/home')
        return redirect(url_for('home.home'))
    
    init_db()  # Refresh connection before select
    mycursor.execute("SELECT stock_id,stock_name,ltp FROM showw where username=%s",(current_user.username,))
        
    stocks=mycursor.fetchall()
    stocks = [{'name': s[0], 'id': s[1],'ltp':s[2]} for s in stocks]
    return render_template('home.html',stocks=stocks)


@home_bp.route('/delete_stock', methods=['POST'])
def delete_stock():
    init_db()  # Refresh connection
    stock_name = request.form.get('stock_name')
    mycursor.execute("select * from showw where stock_name=%s",(stock_name,) )
    stock_name_data=mycursor.fetchone()

    if stock_name_data:
        try:
            init_db()  # Refresh connection before delete
            mycursor.execute(
                "DELETE FROM showw WHERE stock_name = %s AND username = %s",
                (stock_name, current_user.username)
            )
            mydb.commit()
            flash("Stock deleted successfully", "success")
        except Exception as e:
            flash(f"Error deleting stock: {str(e)}", "danger")
    else:
        flash("Invalid stock ID", "danger")
        return redirect('/home')

    return redirect(url_for('home.home'))

    


