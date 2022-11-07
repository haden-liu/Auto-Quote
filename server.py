import psycopg2
import csv
import pandas as pd
import numpy as np
from werkzeug.utils import secure_filename


from flask import Flask, render_template, request, redirect

UPLOAD_FOLDER = '/Users/hangliu/Documents/files'
app = Flask(__name__)

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/calculation')
def calculation():

    return render_template('calculation.html')

@app.route('/calcuation_result', methods= ['POST'])
def calcuation_result():
    loading_port = request.form.get('loadingport')
    discharge_port = request.form.get('dischargingport')
    length = request.form.get('length')
    width = request.form.get('width')
    height = request.form.get('height')
    weight = request.form.get('weight')
    amount = request.form.get('amount')
    
    lenList= request.form.getlist('length')
    widthList = request.form.getlist('width')
    
    print(lenList)
    print(widthList)

    multiply = []
    for value1, value2 in zip(lenList, widthList):
        multiply.append(float(value1) * float(value2))
    print(multiply)

    volume_unit = float(length) * float(width )* float(height) / 1000000
    total_volume = volume_unit * int(amount)
    total_weight = float(weight) * int(amount)

    print(total_volume)
    print(total_weight)

   
    conn = psycopg2.connect('dbname = freight')
    cur = conn.cursor()

    cur.execute('select carrier, freight_rate_min, freight_rate_unit, fuel_rate, valid_date from rates where loading_port = %s and discharging_port = %s', [loading_port,discharge_port])
    result = cur.fetchone()
    print(result)

    carrier, freight_rate_min, freight_rate_unit, fuel_rate, valid_date = result

    if freight_rate_min > max(total_volume * 1000 / 6 * freight_rate_unit, total_weight  * freight_rate_unit):
        total_rate = freight_rate_min
    else:
        total_rate = max(total_volume * 1000 / 6 * freight_rate_unit, total_weight * freight_rate_unit)

    print(total_rate)
    print(valid_date)
    total_fuel = max(total_volume * 1000 / 6 * fuel_rate, total_weight * fuel_rate)


    return render_template('result.html', amount = amount, CBM = round(total_volume, 2), weight = round(total_weight,2), loading_port = loading_port, discharging_port = discharge_port, carrier = carrier, total = round(total_rate, 2), total_fuel = round(total_fuel, 2), valid_date = valid_date)

@app.route('/addrate', methods=['POST', 'GET'])
def addrate():
    loading_port = request.form.get('loadingport')
    discharging_port = request.form.get('dischargingport')
    carrier = request.form.get('carrier')
    minimum_rate = request.form.get('minimum_rate')
    unit_rate = request.form.get("unit_rate")
    fuel_rate = request.form.get('fuel_rate')
    valid_date = request.form.get('valid_date')

    print(discharging_port)


    conn = psycopg2.connect('dbname = freight')
    cur =conn.cursor()

    cur.execute('INSERT INTO rates (carrier,freight_rate_min,freight_rate_unit,fuel_rate,loading_port,discharging_port,valid_date) values (%s,%s,%s,%s,%s,%s,%s)', [carrier, minimum_rate,unit_rate,fuel_rate,loading_port,discharging_port,valid_date])


    conn.commit()
    cur.close()
    conn.close()
    
    return render_template('addrate.html')

@app.route('/manage', methods = ['POST','GET'])
def manage():

        conn = psycopg2.connect('dbname = freight')
        cur =conn.cursor()

        cur.execute('select * from rates where carrier is not null')

        results = cur.fetchall()

        print(results)

        cur.close()
        conn.close()

        return render_template('manage.html')





@app.route('/upload_rate', methods=['POST', 'GET'])
def upload_rate():

    # upload_file = request.files('file')
    # upload_file.save(secure_filename(upload_file.filename))


    df = pd.read_excel("Book1.xlsx")
    print(df)
    print(df['carrier'][0])

    conn = psycopg2.connect('dbname = freight')
    cur =conn.cursor()

    for i in range(len(df)):

        print(df.loc[i, "carrier"], df.loc[i, "valid_date"])
        cur.execute('INSERT INTO rates (carrier,freight_rate_min,freight_rate_unit,fuel_rate,loading_port,discharging_port,valid_date) values (%s,%s,%s,%s,%s,%s,%s)', [df.loc[i, "carrier"], float(df.loc[i, "freight_rate_min"]),float(df.loc[i, "freight_rate_unit"]),float(df.loc[i, "fuel_rate"]),df.loc[i, "loading_port"],df.loc[i, "discharging_port"],df.loc[i, "valid_date"]])

    conn.commit()

    return render_template('addrate.html')






app.run(debug=True)