import psycopg2

from flask import Flask, render_template, request
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

    CBM = int(length) * int(width) * int(height) / 1000000
    print(type(CBM))

    print(loading_port)
   

    conn = psycopg2.connect('dbname = freight')
    cur = conn.cursor()

    cur.execute('select freight_rate_min, freight_rate_unit, freight_rate_weight from rates where loading_port = %s and discharging_port = %s', [loading_port,discharge_port])
    result = cur.fetchone()
    print(result)

    freight_rate_min, freight_rate_unit, freight_rate_weight = result

    total = freight_rate_unit * CBM
    print(total)



    return render_template('result.html')


app.run(debug=True)