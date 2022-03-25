import json
from flask import Flask, Response, redirect, render_template, jsonify, request
import processor

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html', **locals())

@app.route('/send', methods = ["POST"])
def send():
    if request.method == 'POST':
        msg = request.form['question']
        result = processor.chatbot_response(msg)
    print(result)
    return jsonify({'response':result})

@app.route('/about', methods= ['GET'])
def about():
    return render_template('about.html', **locals())

@app.route('/contacts', methods= ['GET'])
def contacts():
    return render_template('contacts.html', **locals())

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='8080', debug=True)