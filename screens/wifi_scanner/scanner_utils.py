import subprocess
import re

def scan_wifi_networks(interface='wlan0'):
    command = f"iwlist {interface} scan"
    try:
        scan_output = subprocess.check_output(command, shell=True).decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"An error occurred: {e}"
    
    networks = {}
    current_cell = None
    for line in scan_output.split('\n'):
        cell_match = re.search("Cell (\d+) - Address: ([\w:]+)", line)
        if cell_match:
            current_cell = cell_match.group(1)
            networks[current_cell] = {'Address': cell_match.group(2)}
        
        if current_cell:
            ssid_match = re.search("ESSID:\"(.+)\"", line)
            if ssid_match:
                networks[current_cell]['ESSID'] = ssid_match.group(1)
            
            signal_match = re.search("Signal level=(\-\d+ dBm)", line)
            if signal_match:
                networks[current_cell]['Signal level'] = signal_match.group(1)
            
            quality_match = re.search("Quality=(\d+/\d+)", line)
            if quality_match:
                networks[current_cell]['Quality'] = quality_match.group(1)
                
            encryption_match = re.search("Encryption key:(on|off)", line)
            if encryption_match:
                networks[current_cell]['Encryption'] = encryption_match.group(1) == 'on'
                
            # Добавляйте дополнительные поля по аналогии, если нужно
                
    return networks

def get_network_interfaces():
    # Выполняем команду `ip link show` для получения списка интерфейсов
    result = subprocess.run(['ip', 'link', 'show'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')

    interfaces = []
    for line in output.split('\n'):
        if ':' in line and not line.startswith(' '):
            # Извлекаем имя интерфейса, которое находится перед двоеточием
            interface_name = line.split(':')[1].strip().split('@')[0]
            interfaces.append(interface_name)

    return interfaces


print(get_network_interfaces())