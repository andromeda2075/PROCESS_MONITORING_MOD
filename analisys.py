
import pickle
from flask import Flask, request, jsonify    
import numpy as np
app = Flask(__name__)
@app.route('/stocks/v1/fetch', methods=['POST'])

def fetch():
    #---get the features to predict---
    details = request.json    #---create the features list for prediction---
    symbol = details["Symbol"]     #---formulate the response to return to client---
    response = {}
    response['symbol'] = symbol
    if symbol == 'AAPL':
        response['price'] = np.random.uniform(168,172)
    if symbol == 'AMD':
        response['price'] = np.random.uniform(140,145)
    if symbol == 'AMZN':
        response['price'] = np.random.uniform(2900,3200)    
    return  jsonify(response)
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)