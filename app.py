from flask import Flask, render_template, request
import requests

app = Flask(__name__)
api_key = 'cfc1a33244804fe4a9e28de139e0a807'

def get_exchange_rate(base_currency, target_currency, amount_to_convert):
    url = f'https://exchange-rates.abstractapi.com/v1/live?api_key={api_key}&base={base_currency}&target={target_currency}'
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        exchange_rates = data.get('exchange_rates', {})
        exchange_rate = exchange_rates.get(target_currency)
        
        if exchange_rate is not None:
            converted_amount = amount_to_convert * exchange_rate
            return converted_amount
        else:
            return None
    else:
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        base_currency = request.form['fromCurrency'].upper() 
        target_currency = request.form['toCurrency'].upper()  
        amount_to_convert = float(request.form['amount'])  

        converted_amount = get_exchange_rate(base_currency, target_currency, amount_to_convert)

        if converted_amount is not None:
            result_message = f"{amount_to_convert} {base_currency} is equal to {converted_amount} {target_currency}"
        else:
            result_message = "Exchange rate not available for the specified currencies."
        
        return render_template('index.html', result_message=result_message)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)