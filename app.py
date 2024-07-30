from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from flask_mysqldb import MySQL
#from waitress import serve
import mysql.connector
import os



app = Flask(__name__)


#MySQL Connection
app.config["MYSQL_HOST"]="localhost"
app.config["MYSQL_USER"]="root"
app.config["MYSQL_PASSWORD"]="12345"
app.config["MYSQL_DB"]="procurement_db"
app.config["MYSQL_CURSORCLASS"]="DictCursor"
mysql = MySQL(app)


#Home Page
@app.route('/')
def index():     
    return render_template('index.html')

#EPROCUREMENT PAGE - DISPLAY
@app.route('/display')
def display():
    con=mysql.connection.cursor()
    sql="SELECT *FROM procurement_data"
    con.execute(sql)
    res=con.fetchall()
    return render_template('display.html',datas=res)


#Create New Record
@app.route("/eprocurement", methods=['GET', 'POST'])
def eprocurement():
    if request.method=='POST':
        serialNumber = request.form['serialNumber']
        itemName = request.form['itemName']
        itemQuantity = request.form['itemQuantity']
        itemUnitPrice = request.form['itemUnitPrice']
        tax = request.form['tax']
        totalPrice = request.form['totalPrice']
        transactionId = request.form['transactionId']
        intenderName = request.form['intenderName']
        supplierName = request.form['supplierName']
        procurementDate = request.form['procurementDate']
        authorityApprovalName = request.form['authorityApprovalName']
        approvalStatus = request.form['approvalStatus']
        deliveryDate = request.form['deliveryDate']
        remarks = request.form['remarks']
        con = mysql.connection.cursor()
        sql = "INSERT INTO procurement_data (serialNumber, itemName, itemQuantity, itemUnitPrice, tax, totalPrice, transactionId, intenderName, supplierName, procurementDate, authorityApprovalName, approvalStatus,  deliveryDate, remarks ) value (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        con.execute(sql,[serialNumber, itemName, itemQuantity, itemUnitPrice, tax, totalPrice, transactionId,  intenderName, supplierName, procurementDate, authorityApprovalName, approvalStatus, deliveryDate, remarks ])
        mysql.connection.commit()
        con.close()
        flash('EProcurement Data Added')
        return redirect(url_for("eprocurement"))
    return render_template("eprocurement.html")


#Update Record
@app.route("/update/<string:id>", methods=['GET','POST'])
def update(id):
    con=mysql.connection.cursor()
    if request.method=='POST':
        
        serialNumber=request.form['serialNumber']
        itemName=request.form['itemName']
        itemQuantity=request.form['itemQuantity']
        itemUnitPrice=request.form['itemUnitPrice']
        tax=request.form['tax']
        totalPrice=request.form['totalPrice']
        transactionId=request.form['transactionId']
        intenderName=request.form['intenderName']
        supplierName=request.form['supplierName']
        procurementDate=request.form['procurementDate']
        authorityApprovalName=request.form['authorityApprovalName']
        approvalStatus=request.form['approvalStatus']
        deliveryDate=request.form['deliveryDate']
        remarks=request.form['remarks']
        sql="UPDATE procurement_data SET serialNumber=%s, itemName=%s, itemQuantity=%s, itemUnitPrice=%s, tax=%s, totalPrice=%s, transactionId=%s,  intenderName=%s, supplierName=%s, procurementDate=%s, authorityApprovalName=%s, approvalStatus=%s, deliveryDate=%s, remarks=%s  WHERE id=%s"
        con.execute(sql,[serialNumber, itemName, itemQuantity, itemUnitPrice, tax, totalPrice, transactionId,  intenderName, supplierName, procurementDate, authorityApprovalName, approvalStatus, deliveryDate, remarks, id])
        mysql.connection.commit()
        con.close()
        flash('Procurement Data Updated')
        return redirect(url_for("display"))
    
    con=mysql.connection.cursor()
    sql="SELECT * FROM procurement_data WHERE id=%s"
    con.execute(sql,[id])
    res=con.fetchone()
    return render_template("update.html", datas=res)


#DELETE Record
@app.route("/delete/<string:id>", methods=['GET','POST'])
def delete(id):
    con=mysql.connection.cursor()
    sql="DELETE  FROM procurement_data WHERE id=%s"
    con.execute(sql,[id])
    mysql.connection.commit()
    con.close()
    flash('Data Deleted Successfully')
    return redirect(url_for("display"))
    

#Main Function
if __name__ == "__main__":
    app.secret_key="abc123"
    app.run(debug=True)

