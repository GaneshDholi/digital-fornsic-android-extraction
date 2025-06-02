from flask import Flask, render_template, jsonify, request
from mobile_extractor import check_device, extract_sms, extract_contacts, extract_calls, pull_dcim
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recover/android', methods=['GET'])
def recover_android():
    result = {
        "device": check_device(),
        "sms": extract_sms(),
        "contacts": extract_contacts(),
        "calls": extract_calls(),
        "dcim": pull_dcim()
    }
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
