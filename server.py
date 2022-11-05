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
    amount = request.form.get('amount')

    volume_unit = int(length) * int(width) * int(height) / 1000000
    total_volume = volume_unit * int(amount)
    total_weight = float(weight) * int(amount)

    print(total_volume)
    print(total_weight)

   
    conn = psycopg2.connect('dbname = freight')
    cur = conn.cursor()

    cur.execute('select carrier, freight_rate_min, freight_rate_unit, freight_rate_weight from rates where loading_port = %s and discharging_port = %s', [loading_port,discharge_port])
    result = cur.fetchone()
    print(result)

    carrier, freight_rate_min, freight_rate_unit, freight_rate_weight = result

    if freight_rate_min > max(total_volume * freight_rate_unit, total_weight / 1000 * freight_rate_unit):
        total_rate = freight_rate_min
    else:
        total_rate = max(total_volume * freight_rate_unit, total_weight / 1000 * freight_rate_unit)

    print(total_rate)


 



    return render_template('result.html', amount = amount, CBM = total_volume, weight = total_weight, loading_port = loading_port, discharging_port = discharge_port, carrier = carrier, total = total_rate)


app.run(debug=True)