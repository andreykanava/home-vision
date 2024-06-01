import os

# Относительный путь к вашей папке
folder_path = '/Users/andrejkanava/Documents/home-vision/screens/VPN/configs/'
print(os.getcwd())
# Получение списка файлов с расширением .ovpn и удаление расширения
ovpn_files = [os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.endswith('.ovpn')]

print(sorted(ovpn_files))