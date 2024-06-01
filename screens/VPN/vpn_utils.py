import subprocess
import time
import os

def connect_vpn(config_path, cred_path):
    try:
        command = f'sudo openvpn --config {config_path} --auth-user-pass {cred_path} &'
        
        subprocess.run(command, shell=True, check=True)
        
        time.sleep(10)
        
        print("VPN connected.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while connecting to the VPN: {e}")

def disconnect_vpn():
    try:
        command = 'sudo pkill openvpn'
        
        subprocess.run(command, shell=True, check=True)
        
        print("VPN disconnected.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while disconnecting from the VPN: {e}")
