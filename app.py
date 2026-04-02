from flask import Flask, render_template, request, redirect
import mysql.connector

import os
from urllib.parse import urlparse

app = Flask(__name__)

# 🔥 GET DATABASE URL
db_url = os.getenv("mysql://root:ZcNowEIUJqcTcHbrgKymNqTHIgiEErsX@centerbeam.proxy.rlwy.net:23028/railway")

# 👉 fallback for local testing (IMPORTANT)
if not db_url:
    db_url = "mysql://root:ZcNowEIUJqcTcHbrgKymNqTHIgiEErsX@centerbeam.proxy.rlwy.net:23028/railway"

url = urlparse(db_url)

# 🔥 DATABASE CONNECTION
db = mysql.connector.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    database=url.path[1:],   # ✅ correct way (remove "/")
    port=url.port
)

cursor = db.cursor()

# HOME (Single Page - shows all data)
@app.route('/')
def index():
    cursor.execute("SELECT * FROM customer")
    data = cursor.fetchall()
    return render_template("index.html", customers=data)

# INSERT (Create)
@app.route('/insert', methods=['POST'])
def insert():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

    sql = "INSERT INTO customer (name, mobile, amount, location) VALUES (%s, %s, %s, %s)"
    values = (name, mobile, amount, location)

    cursor.execute(sql, values)
    db.commit()

    return redirect('/')

# DELETE
@app.route('/delete/<mobile>')
def delete(mobile):
    cursor.execute("DELETE FROM customer WHERE mobile = %s", (mobile,))
    db.commit()
    return redirect('/')

# UPDATE
@app.route('/update', methods=['POST'])
def update():
    name = request.form['name']
    mobile = request.form['mobile']
    amount = request.form['amount']
    location = request.form['location']

    sql = """
        UPDATE customer 
        SET name=%s, amount=%s, location=%s 
        WHERE mobile=%s
    """
    values = (name, amount, location, mobile)

    cursor.execute(sql, values)
    db.commit() 

    return redirect('/')

# RUN SERVER
if __name__ == "__main__":
    app.run(debug=True)