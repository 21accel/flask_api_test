#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, jsonify, request, Response
from flask_mysqldb import MySQL
import random, string
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_test'
mysql = MySQL(app)


@app.route('/api/token', methods=['GET'])
def get_token():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO token(id) VALUES (%s)", [token])
    mysql.connection.commit()
    cur.close()
    output = [{ 'Your token': token }]
    return jsonify(output)

@app.route('/api/users', methods=['GET'])
def get_all_users():
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO token(id) VALUES (%s)", [token])
    mysql.connection.commit()
    cur.close()
    output = [{ 'Your token': token }]
    return jsonify(output)

@app.route('/api/users/signup', methods=['POST'])
def signup():
    # headers = {"Content-Type": "application/json"}
    user = request.json['user']
    Name = user['name']
    Address = user['address']
    Username = user['username']
    Email = user['email']
    Encrypted_password = user['encrypted_password']
    Phone = user['phone']
    City = user['city']
    Country = user['country']
    Postcode = user['postcode'] 
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO user(name, address, username, password, email, phone, country, city, postcode) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (Name, Address, Username, Encrypted_password, Email, Phone, Country, City, Postcode))
    mysql.connection.commit()
    cur.close()
    token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
    output = [{ 'email':Email, 'username': Username, 'token': token }]
    return jsonify(output)

@app.route('/api/users/signin', methods=['POST'])
def signin():
    login = request.json
    Email = login['email']
    Password = login['password']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user WHERE email = %s", [Email])
    mysql.connection.commit()
    result = cur.fetchall()
    cur.close()
    if len(result) == 1:
        if Password in result[0][2]:
            token = ''.join(random.choices(string.ascii_letters + string.digits, k=16))
            output = [{ 'email':Email, 'username': result[0][1], 'token': token }]
            return jsonify(output)
        else:
            output = [{ 'code':'403', 'error_msg': 'password wrong!'}]
            return jsonify(output)
    else:
        output = [{'code':'404','error_msg':'user not found'}]
        return jsonify(output)

@app.route('/api/shopping', methods=['POST'])
def create_new_shopping():
    shopping = request.json
    Created_date = shopping['createddate']
    Name = shopping['name']
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO shopping(name, created_date) VALUES (%s, %s)", (Name, Created_date))
    id = cur.lastrowid
    mysql.connection.commit()
    cur.close()
    output = [{'ID':id,'name':Name, 'created_date':Created_date}]
    return jsonify(output)


@app.route('/api/shopping/<id>', methods=['PUT'])
def update_new_shopping(id):
    shopping = request.json
    Created_date = shopping['createddate']
    Name = shopping['name']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM shopping WHERE id = %s", [id])
    mysql.connection.commit()
    result = cur.fetchall()
    cur.close()
    if len(result) == 1:
        cur = mysql.connection.cursor()
        cur.execute("UPDATE shopping SET name = %s, created_date = %s WHERE id=%s", (Name, Created_date, id))
        mysql.connection.commit()
        cur.close()
        output = [{ 'id':id, 'name': Name, 'createddate': Created_date }]
        return jsonify(output)
    else:
        output = [{'code':'404','error_msg':'item not found'}]
        return jsonify(output)


app.run(debug=True)