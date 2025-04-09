from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from ai_agent import get_ai_response
import os

# Environment variables
load_dotenv()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    message = request.json.get('message')
    if not message:
        return jsonify({'error': 'No message provided'}), 400
    
    response = get_ai_response(message)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)