#!/usr/bin/env python3

import subprocess
import os
import csv
from datetime import datetime
import time

output_dir = "logs_dataset"
csv_file = os.path.join(output_dir, "logs_summary.csv")

# Create output directory and CSV if not present
os.makedirs(output_dir, exist_ok=True)
if not os.path.exists(csv_file):
    with open(csv_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'pod_name', 'errors', 'logs'])

def get_pod_logs(pod_name):
    try:
        logs = subprocess.check_output(['kubectl', 'logs', pod_name], stderr=subprocess.STDOUT).decode()
        return logs
    except subprocess.CalledProcessError as e:
        return e.output.decode()

def extract_errors(logs):
    error_lines = []
    for line in logs.split('\n'):
        if 'error' in line.lower() or 'emerg' in line.lower() or 'fail' in line.lower() or 'warn' in line.lower():
            error_lines.append(line)
    return '\n'.join(error_lines)

def main():
    while True:
        # Get all pod names
        pod_list = subprocess.check_output(['kubectl', 'get', 'pods', '-o', 'jsonpath={.items[*].metadata.name}']).decode().split()

        for pod_name in pod_list:
            logs = get_pod_logs(pod_name)
            errors = extract_errors(logs)

            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            error_file = os.path.join(output_dir, f"{pod_name}_errors.log")
            log_file = os.path.join(output_dir, f"{pod_name}_full.log")

            # Append errors and logs
            with open(error_file, 'a') as f:
                f.write(f"\n--- {timestamp} ---\n{errors}\n")

            with open(log_file, 'a') as f:
                f.write(f"\n--- {timestamp} ---\n{logs}\n")

            # Append to CSV
            with open(csv_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([pod_name ,timestamp , errors.strip(), logs.strip()])

            # Display errors in terminal
            print(f"\n=== Logs for pod: {pod_name} ===")
            if errors.strip():
                print("--- Errors found:")
                print(errors)
            else:
                print("--- No errors found.")

        # Sleep for 60 seconds before next check
        time.sleep(60)

if __name__ == "__main__":
    main()
