import os
import subprocess
from datetime import datetime
import uuid

def run_adb_command(cmd):
    try:
        result = subprocess.check_output(["adb"] + cmd, stderr=subprocess.DEVNULL)
        return result.decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

def recover_deleted_files():
    # Format: YYYY-MM-DD_HH-MM-SS
    time_stamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_dir = os.path.join("data-recover", f"recovered_{time_stamp}")
    os.makedirs(session_dir, exist_ok=True)

    deleted_files = [
        "/sdcard/Android/data/com.whatsapp/Media/.Statuses",
        "/sdcard/WhatsApp/Databases/msgstore.db.crypt14",
        "/sdcard/DCIM/.thumbnails"
    ]

    extracted = {}

    for file_path in deleted_files:
        local_filename = os.path.join(session_dir, os.path.basename(file_path))
        pull_result = run_adb_command(["adb", "pull", file_path, local_filename])
        if os.path.exists(local_filename):
            extracted[file_path] = local_filename
        else:
            extracted[file_path] = None

    return session_dir, extracted
