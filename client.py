import socket
import os
import sys

'''Thisfile=sys.argv[0]     #полный путь к файлу
Thisfile_name=os.path.basename(Thisfile)       # название файла и расширение
user_path=os.path.expanduser('~')
if not os.path.exists(f"{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\{Thisfile_name}"):
        os.system(f'copy "{Thisfile}" "{user_path}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"')
'''


def client():
    host = # необходимый ip-адресс
    port = 5000
    client_socket = socket.socket()
    client_socket.connect((host, port))
    #message = "Привет"
    message=input('Введите сообщение: ')
    while message.lower().strip() != 'пока':
        message=client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        print('Сообщение от сервера: ' + data)
        if data == 'Пока':
            break
        message = input('Введите сообщение: ')
    client_socket.close()


if __name__ == '__main__':
    while True:
        try:
            client()
        except ConnectionRefusedError:
            print('try')
            continue

