import os
import hashlib
import time
import yaml
import smtplib
from email.mime.text import MIMEText

def load_config(config_path='config.yaml'):
    with open(config_path, 'r') as f:
        return yaml.safe_load(f)

def hash_file(filepath):
    sha256 = hashlib.sha256()
    try:
        with open(filepath, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b''):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return None

def scan_directory(directory):
    file_hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            hash_val = hash_file(path)
            if hash_val:
                file_hashes[path] = hash_val
    return file_hashes

def send_email(subject, body, config):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = config['email']['from']
    msg['To'] = config['email']['to']
    try:
        with smtplib.SMTP_SSL(config['email']['smtp_server'], config['email']['smtp_port']) as server:
            server.login(config['email']['username'], config['email']['password'])
            server.sendmail(config['email']['from'], [config['email']['to']], msg.as_string())
    except Exception as e:
        print(f"Failed to send email: {e}")

def monitor(config):
    directory = config['monitor']['directory']
    interval = config['monitor']['interval']
    alert_email = config['monitor']['alert_email']
    print(f"Monitoring directory: {directory}")
    prev_hashes = scan_directory(directory)
    while True:
        time.sleep(interval)
        curr_hashes = scan_directory(directory)
        added = set(curr_hashes.keys()) - set(prev_hashes.keys())
        removed = set(prev_hashes.keys()) - set(curr_hashes.keys())
        modified = {f for f in curr_hashes if f in prev_hashes and curr_hashes[f] != prev_hashes[f]}
        if added or removed or modified:
            alert = []
            if added:
                alert.append(f"Added: {', '.join(added)}")
            if removed:
                alert.append(f"Removed: {', '.join(removed)}")
            if modified:
                alert.append(f"Modified: {', '.join(modified)}")
            alert_msg = '\n'.join(alert)
            print(f"[ALERT] {alert_msg}")
            if alert_email:
                send_email("File Integrity Alert", alert_msg, config)
        prev_hashes = curr_hashes

if __name__ == "__main__":
    config = load_config()
    monitor(config)
