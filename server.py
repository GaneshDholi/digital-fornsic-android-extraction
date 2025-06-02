import os
from flask import Flask, render_template, request, redirect, url_for
from extractors import android_extractor  # your android extractor module
from flask import Flask, render_template, request, redirect, url_for, flash
from extractors import android_extractor as ae
import subprocess
from flask import jsonify
import shutil
from flask import send_file

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/recover/android')
def recover_android():
    return redirect(url_for('connect'))

@app.route('/connect')
def connect():
    return render_template('connect.html')

@app.route('/connect2')
def connect2():
    return render_template('connect2.html')

@app.route('/select', methods=['GET', 'POST'])
def select_data():
    if request.method == 'POST':
        selected_types = request.form.getlist('data_type')
        if not selected_types:
            flash("Please select at least one data type.")
            return redirect(url_for('select_data'))

        device = ae.check_device()
        if not device:
            flash("No device connected. Please connect a device with ADB enabled.")
            return redirect(url_for('select_data'))

        session_dir = ae.create_session_folder()
        results = {}

        for data_type in selected_types:
            if data_type == 'sms':
                results['sms'] = ae.extract_sms(session_dir)
            elif data_type == 'contacts':
                results['contacts'] = ae.extract_contacts(session_dir)
            elif data_type == 'calls':
                results['calls'] = ae.extract_calls(session_dir)
            elif data_type == 'dcim':
                results['dcim'] = ae.pull_dcim(session_dir)
            elif data_type == 'audio':
                results['audio'] = ae.pull_audio(session_dir)
            elif data_type == 'video':
                results['video'] = ae.pull_video(session_dir)
            elif data_type == 'documents':
                results['documents'] = ae.pull_documents(session_dir)
            elif data_type == 'location':
                results['location'] = ae.extract_location(session_dir)
            elif data_type == 'device_info':
                # Placeholder: Add device info extractor in future
                results['device_info'] = ae.run_adb_command("adb shell getprop")

        return render_template("result.html", results=results, session_dir=session_dir)

    return render_template("select.html")
    if request.method == 'POST':
        # Get selected options from form
        selected_data = request.form.getlist('data_type')
        session_dir = android_extractor.create_session_folder()

        # Run extraction based on selection
        extracted_files = {}
        if 'sms' in selected_data:
            extracted_files['sms'] = android_extractor.extract_sms(session_dir)
        if 'contacts' in selected_data:
            extracted_files['contacts'] = android_extractor.extract_contacts(session_dir)
        if 'calls' in selected_data:
            extracted_files['calls'] = android_extractor.extract_calls(session_dir)
        if 'dcim' in selected_data:
            extracted_files['dcim'] = android_extractor.pull_dcim(session_dir)
        if 'audio' in selected_data:
            extracted_files['audio'] = android_extractor.pull_audio(session_dir)
        if 'video' in selected_data:
            extracted_files['video'] = android_extractor.pull_video(session_dir)
        if 'documents' in selected_data:
            extracted_files['documents'] = android_extractor.pull_documents(session_dir)

        # Pass session_dir and extracted_files info to result page
        return render_template('result.html', session_dir=session_dir, extracted_files=extracted_files)

    # GET: show selection form
    return render_template('select.html')

@app.route('/download/<path:session_dir>')
def download_zip(session_dir):
    zip_path = f"{session_dir}.zip"
    if not os.path.exists(zip_path):
        shutil.make_archive(session_dir, 'zip', session_dir)
    return send_file(zip_path, as_attachment=True)

def read_text_file_safe(path):
    if path and os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return None


@app.route('/result')
def result():
    # This route can be optional if you always redirect to /result with data after extraction
    return "Extraction complete. You should come here only after extraction."

@app.route('/check-device')
def check_device():
    try:
        result = subprocess.check_output(['adb', 'devices'], universal_newlines=True)
        lines = result.strip().split('\n')[1:]  # Skip the header
        devices = [line for line in lines if line.strip() and 'device' in line]
        return jsonify({'connected': len(devices) > 0})
    except Exception as e:
        print("ADB error:", e)
        return jsonify({'connected': False})
if __name__ == '__main__':
    app.run(debug=True)
