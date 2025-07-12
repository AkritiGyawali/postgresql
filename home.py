from flask import Blueprint, render_template,request,redirect , flash,url_for, request
from flask_login import login_required,current_user

import mysql.connector
import httpx
import os
from dotenv import load_dotenv
load_dotenv()


stock_list= {}
api_url = 'https://nepalstock.onrender.com/securityDailyTradeStat/58'
home_bp= Blueprint('home', __name__) 
sqhost=os.getenv('host')
squser=os.getenv('username')
sqpassword=os.getenv('password')
sqdatabase=os.getenv('database')
mydb=mysql.connector.connect(

    host=sqhost,
    user=squser,
    password=sqpassword,
    database=sqdatabase
)

mycursor=mydb.cursor()

@home_bp.route('/home',methods=['POST','GET'])
@login_required
def home():
    
 
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
                    mycursor.execute("INSERT INTO showw(stock_name,stock_id,ltp,username)VALUES(%s,%s,%s,%s)",(stock_list['name'],stock_list['id'],stock_list['ltp'],current_user.username))
                    mydb.commit()
                    found = True
                    break
                
                   

            if not found:
                flash(f"Invalid stock name", 'danger')
                return redirect('/home')
        return redirect(url_for('home.home'))
    mycursor.execute("SELECT stock_id,stock_name,ltp FROM showw where username=%s",(current_user.username,))
        
    stocks=mycursor.fetchall()
    stocks = [{'name': s[0], 'id': s[1],'ltp':s[2]} for s in stocks]
    return render_template('home.html',stocks=stocks)


@home_bp.route('/delete_stock', methods=['POST'])
def delete_stock():
      
    stock_name = request.form.get('stock_name')
    mycursor.execute("select * from showw where stock_name=%s",(stock_name,) )
    stock_name_data=mycursor.fetchone()

    if stock_name_data:
        try:
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

    


