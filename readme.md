📱 Mobile Forensic Analysis System
🔍 Overview
Mobile Forensic Analysis System is a web-based forensic tool built using Flask and Android Debug Bridge (ADB). It enables forensic investigators to extract critical data such as:

📁 Audio, Video, Images, Documents

📍 Location Data

📞 Call Logs

👤 Contacts

📱 Device Information

...from Android devices without rooting.

⚠️ Due to Android security restrictions, deleted data and encrypted social media app data (e.g., WhatsApp, Facebook, Instagram) cannot be recovered unless root access is granted.

⚙️ Features
Web UI for forensic data extraction

One-click ADB-based extraction for connected Android devices

Organized output folders for different data types

Device information gathering

Compatible with Windows/Linux

📁 Folder Structure
csharp
Copy
Edit
mobile-forensic-analysis/
│
├── app.py                  # Flask backend
├── templates/              # HTML UI templates
│   ├── index.html
│   ├── connect.html
│   ├── result.html
│   └── select.html
├── static/                 # Static files (CSS, JS, images)
├── extractions/           # Extracted data stored here
│   ├── audio/
│   ├── video/
│   ├── images/
│   ├── documents/
│   ├── call_logs/
│   ├── contacts/
│   └── location/
├── requirements.txt        # Python dependencies
└── README.md
🖥️ Installation & Setup
Prerequisites
Python 3.8+

ADB installed and added to PATH

Android device with USB Debugging enabled

Installation Steps
bash
Copy
Edit
# Clone the repository
git clone https://github.com/yourusername/mobile-forensic-analysis.git
cd mobile-forensic-analysis

# Install dependencies
pip install -r requirements.txt

# Run the Flask app
python app.py
Access the Tool
Open your browser and go to:
http://127.0.0.1:5000

🔌 How to Use
Connect an Android device via USB with USB Debugging enabled.

Launch the web app.

Select data types to extract.

Click "Extract" to begin the forensic process.

Download and review results.

📸 Screenshots
Include screenshots like:

UI Homepage

Data selection screen

Extraction in progress

Final result folder

🛡️ Disclaimer
This tool is designed for forensic and legal use only. The authors are not responsible for any misuse of this software. Always ensure you have legal authorization before extracting data from a device.

