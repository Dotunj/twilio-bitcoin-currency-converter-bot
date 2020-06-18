from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app= Flask(__name__)

@app.route('/incoming/twilio', methods=['POST'])
def incoming_twilio():
    incoming_message=request.form['Body'].lower()
    message= incoming_message.split()
    resp= MessagingResponse()
    msg=resp.message()

    if 'hello' in incoming_message:
        reply = standard_response_format()
        msg.body(reply)
        return str(resp)

    if len(message) < 4:
       reply = standard_response_format()
       msg.body(reply)
       return str(resp)
    
    btc_unit = message[1]
    currency_code = message[4].upper()
    r = requests.get("https://api.coinbase.com/v2/exchange-rates?currency=BTC")
    if r.status_code == 200:
        data = r.json()
        rates = data['data']['rates']
        if currency_code in rates:
            unit_rate = rates[currency_code]
            unit_conversion = get_unit_conversion(btc_unit, unit_rate)
            reply=f"{btc_unit} BTC is {unit_conversion:,} {currency_code}"
        else:
           reply=f"{currency_code} is not a valid currency code"
    else:
        reply= "Something went wrong"
    msg.body(reply)
    return str(resp)

def standard_response_format():
    return ("Welcome to the Bitcoin Currency Converter bot!\n\n" 
            "Please use the following format to chat with the bot: \n" 
            "Convert 1 BTC to USD \n"
            "1 is the number of BTC unit you would like to convert \n"
            "USD is the currency code you would like to convert too \n")

def get_unit_conversion(unit, unit_rate):
    return round(round(float(unit_rate), 2) * float(unit), 2)

if __name__ == '__main__':
    app.run()