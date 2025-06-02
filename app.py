from flask import Flask, render_template, jsonify, redirect, url_for
from data_recover import recover_deleted_files
import subprocess
import os

app = Flask(__name__)
connected = False
results = {}
session_dir = ""

@app.route('/')
def home():
    return render_template('connect2.html')

@app.route('/check-device')
def check_device():
    global connected
    try:
        output = subprocess.check_output(["adb", "devices"]).decode()
        connected = 'device' in output and not 'unauthorized' in output
    except:
        connected = False
    return jsonify({'connected': connected})

@app.route('/select')
def extract():
    global session_dir, results
    session_dir, results = recover_deleted_files()
    return redirect(url_for('result_page'))

@app.route('/result2.html')
def result_page():
    return render_template("result2.html", results=results, session_dir=session_dir)

@app.route('/download_zip')
def download_zip():
    import shutil
    zip_path = f"{session_dir}.zip"
    shutil.make_archive(session_dir, 'zip', session_dir)
    return redirect(url_for('static', filename=os.path.basename(zip_path)))

if __name__ == '__main__':
    app.run(debug=True)
