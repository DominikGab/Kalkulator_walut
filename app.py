import requests
import csv
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/waluty', methods=['GET', 'POST'])
def rates():
    response = requests.get("http://api.nbp.pl/api/exchangerates/tables/C?format=json")
    data = response.json()

    currencies_data = ['currency', 'code', 'bid', 'ask']
    currencies = []
    for rate in data[0]['rates']:
        currencies.append([rate['currency'], rate['code'], rate['bid'], rate['ask']])
        
    selected_currency = None
    conversion_result = None
    if request.method == 'POST':
        selected_currency = request.form['currency']
        amount = float(request.form['amount'])
        for currency in currencies:
            if currency[1] == selected_currency:
                conversion_result = currency[2] * amount

    return render_template('form.html', currencies=currencies, currencies_data=currencies_data, selected_currency=selected_currency, conversion_result=conversion_result)

if __name__ == '__main__':
    app.run(debug=True)