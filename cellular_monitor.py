#!/usr/bin/env python3
import paramiko
import time
import sys
import re
import os
import json

CONFIG_PATH = os.path.expanduser("~/.config/cellmon_config.json")

# ANSI color codes
RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

def load_config():
    if not os.path.exists(CONFIG_PATH):
        print("Configuration file not found. Please run the installer.")
        sys.exit(1)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def colorize_metric(name, value, unit):
    try:
        val = float(value)
    except ValueError:
        return f"{value}{unit}"
    if name == "RSSI":
        if val <= -100: return f"{RED}{value}{unit}{RESET}"
        elif val <= -85: return f"{YELLOW}{value}{unit}{RESET}"
        else: return f"{GREEN}{value}{unit}{RESET}"
    if name == "RSRP":
        if val <= -110: return f"{RED}{value}{unit}{RESET}"
        elif val <= -95: return f"{YELLOW}{value}{unit}{RESET}"
        else: return f"{GREEN}{value}{unit}{RESET}"
    if name == "RSRQ":
        if val <= -19: return f"{RED}{value}{unit}{RESET}"
        elif val <= -12: return f"{YELLOW}{value}{unit}{RESET}"
        else: return f"{GREEN}{value}{unit}{RESET}"
    if name == "SNR":
        if val < 5: return f"{RED}{value}{unit}{RESET}"
        elif val < 13: return f"{YELLOW}{value}{unit}{RESET}"
        else: return f"{GREEN}{value}{unit}{RESET}"
    return f"{value}{unit}"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def poll_cellular(ip, username, password):
    pattern = re.compile(r"(RSSI|RSRP|RSRQ|SNR)\s*=\s*([-+]?\d*\.?\d*)\s*(dB|dBm)")
    ssh = None
    while True:
        try:
            if ssh is None or not ssh.get_transport() or not ssh.get_transport().is_active():
                print(f"Connecting to {ip}...")
                ssh = paramiko.SSHClient()
                ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                ssh.connect(ip, username=username, password=password, look_for_keys=False, timeout=15)
                print("Connected.")
            stdin, stdout, stderr = ssh.exec_command("show cellular 0/2/0 radio")
            output = stdout.read().decode()
            metrics = {}
            for line in output.splitlines():
                match = pattern.search(line)
                if match:
                    name, value, unit = match.groups()
                    metrics[name] = colorize_metric(name, value, unit)
            clear_screen()
            print(f"Cellular RF Monitor - {ip}")
            print(f"Last update: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            for m in ["RSSI","RSRP","RSRQ","SNR"]:
                print(f"{m}: {metrics.get(m,'N/A')}")
        except Exception as e:
            clear_screen()
            print(f"{RED}Error: {e}{RESET}")
            print("Reconnecting in 5 seconds...")
            time.sleep(5)
            ssh = None
            continue
        time.sleep(5)

if __name__ == "__main__":
    config = load_config()
    if len(sys.argv) > 1:
        ip_address = sys.argv[1]
    else:
        ip_address = input("Enter device IP: ")
    poll_cellular(ip_address, config["username"], config["password"])
