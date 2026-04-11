from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()
app = Flask(__name__, template_folder='.', static_folder='.')

client = Anthropic()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json.get('data')
    
    # Call Claude API for workforce gap analysis
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Analyze this workforce data for gaps and provide insights:\n\n{data}"
            }
        ]
    )
    
    result = message.content[0].text
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)