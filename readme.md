mobile_forensic_tool/
│
├── server.py                      # Flask server - API routes
├── templates/
|   ├── connect.html
|   ├── result.html
|   ├── select.html
│   └── index.html                 # Your provided frontend HTML
|   
│
├── extractors/
│   ├── __init__.py
│   ├── android_extractor.py
│   ├── whatsapp_extractor.py
│   ├── facebook_extractor.py
│   └── ... (more as needed)
│
└── extracted_data/                # Extracted output gets saved here
