import subprocess

def scan_wifi_networks(interface='wlan0'):
    cmd = ["sudo", "iwlist", interface, "scan"]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    
    networks = []
    for line in stdout.decode('utf-8').split('\n'):
        if "ESSID" in line:
            networks.append(line.split('"')[1])

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