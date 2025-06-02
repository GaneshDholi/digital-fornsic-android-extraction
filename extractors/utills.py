import subprocess

def run_adb_command(command):
    result = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()
