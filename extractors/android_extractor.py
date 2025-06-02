import subprocess
import os
from datetime import datetime
import shutil
import re

def run_adb_command(command):
    try:
        proc = subprocess.run(command, shell=True, capture_output=True)
        output = proc.stdout.decode('utf-8', errors='ignore')
        error = proc.stderr.decode('utf-8', errors='ignore')
        if error.strip():
            return output + "\nERROR: " + error
        return output
    except Exception as e:
        return f"Exception: {str(e)}"

def create_session_folder():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_dir = os.path.join("extracted_data", f"extraction_{timestamp}")
    os.makedirs(session_dir, exist_ok=True)
    for subdir in ["Images", "Audio", "Video", "Documents"]:
        os.makedirs(os.path.join(session_dir, subdir), exist_ok=True)
    return session_dir

def check_device():
    output = run_adb_command("adb devices")
    devices = [line for line in output.splitlines() if "\tdevice" in line]
    return devices[0].split()[0] if devices else None

def extract_sms(session_dir):
    sms_data = run_adb_command("adb shell content query --uri content://sms/")
    if sms_data.strip():
        file_path = os.path.join(session_dir, "sms.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(sms_data)
            
        static_dir = "static"
        os.makedirs(static_dir, exist_ok=True)
        static_path = os.path.join(static_dir, "sms.txt")
        shutil.copy(file_path, static_path)

        return "sms.txt"
    
    return None

def extract_contacts(session_dir):
    contacts = run_adb_command("adb shell content query --uri content://contacts/phones/")
    if contacts.strip():
        file_path = os.path.join(session_dir, "contacts.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(contacts)
    
        static_dir = "static"
        os.makedirs(static_dir, exist_ok=True)
        static_path = os.path.join(static_dir, "contacts.txt")
        shutil.copy(file_path, static_path)

        return "contacts.txt"
    
    return None

def extract_calls(session_dir):
    calls = run_adb_command("adb shell content query --uri content://call_log/calls/")
    if calls.strip():
        file_path = os.path.join(session_dir, "call_logs.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(calls)
        
        static_dir = "static"
        os.makedirs(static_dir, exist_ok=True)
        static_path = os.path.join(static_dir, "call_logs.txt")
        shutil.copy(file_path, static_path)

        return "call_logs.txt"
    return None

def extract_location(session_dir):
    location_data = run_adb_command("adb shell dumpsys location")
    if location_data.strip():
        local_path = os.path.join(session_dir, "location.txt")
        with open(local_path, "w", encoding="utf-8") as f:
            f.write(location_data)

        # Save to static folder
        static_path = os.path.join("static", "location.txt")
        os.makedirs("static", exist_ok=True)
        shutil.copy(local_path, static_path)

        # Match latitude and longitude from any provider
        match = re.search(
            r'last location=Location\[[a-zA-Z0-9_]+ ([\-+]?\d{1,3}\.\d+),\s*([\-+]?\d{1,3}\.\d+)', 
            location_data
        )

        if match:
            lat, lon = match.groups()
            summary = (
                f"Latitude: {lat}, Longitude: {lon}\n"
                f"Google Maps: https://www.google.com/maps?q={lat},{lon}"
            )
        else:
            summary = "Location Information"

        return {
            "path": static_path,
            "summary": summary
        }

    return None
def pull_files_by_extension(session_dir, extensions, subfolder):
    search_dirs = ["/sdcard", "/storage/emulated/0"]
    destination = os.path.join(session_dir, subfolder)
    os.makedirs(destination, exist_ok=True)

    pulled_files = []
    for base_dir in search_dirs:
        for ext in extensions:
            find_command = f'adb shell find "{base_dir}" -type f -iname "*.{ext}"'
            result = run_adb_command(find_command)
            files = result.strip().splitlines()

            for file in files:
                file = file.strip()
                if file:
                    filename = os.path.basename(file)
                    target_path = os.path.join(destination, filename)
                    pull_command = f'adb pull "{file}" "{target_path}"'
                    run_adb_command(pull_command)
                    pulled_files.append(filename)

    return {
        "path": destination,
        "count": len(pulled_files),
        "files": pulled_files
    } if pulled_files else None

def pull_images(session_dir):
    image_extensions = ["jpg", "jpeg", "png"]
    return pull_files_by_extension(session_dir, image_extensions, "Images")

def pull_audio(session_dir):
    audio_extensions = ["mp3", "wav", "aac", "ogg", "m4a"]
    return pull_files_by_extension(session_dir, audio_extensions, "Audio")

def pull_video(session_dir):
    video_extensions = ["mp4", "mkv", "avi", "mov", "flv"]
    return pull_files_by_extension(session_dir, video_extensions, "Video")

def pull_documents(session_dir):
    doc_extensions = ["pdf", "doc", "docx", "ppt", "pptx", "txt", "xls", "xlsx"]
    return pull_files_by_extension(session_dir, doc_extensions, "Documents")

# Optional test run
if __name__ == "__main__":
    device = check_device()
    if not device:
        print("No device connected.")
    else:
        print(f"Device connected: {device}")
        session = create_session_folder()
        print("Extracting images...")
        print(pull_images(session))
        print("Extracting audio...")
        print(pull_audio(session))
        print("Extracting videos...")
        print(pull_video(session))
        print("Extracting documents...")
        print(pull_documents(session))
        print("Extracting SMS...")
        extract_sms(session)
        print("Extracting contacts...")
        extract_contacts(session)
        print("Extracting call logs...")
        extract_calls(session)
        print("Extracting location info...")
        extract_location(session)
        print(f"Extraction complete. Session folder: {session}")
