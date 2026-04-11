from flask import Flask, request, jsonify
import os
from dotenv import load_dotenv
import requests

load_dotenv()
app = Flask(__name__)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json.get('data')
    # Here you would include the call to Claude API with the data
    result = "This is a simulated result for: " + data
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)