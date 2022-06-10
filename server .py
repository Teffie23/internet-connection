import socket
import time
def server():
    host = socket.gethostname()
    # print(socket.gethostbyname(host))
    port = 5000
    server_socket = socket.socket()
    server_socket.bind((host, port))
    server_socket.listen(1)
    conn, address = server_socket.accept()
    print('подключился: ', str(address))
    print('количество подключенных пользователей: ', len(address))

    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(f'сообщение от пользователя {address[0]}: ' + str(data))
        data = input('Введите сообщение: ')
        conn.send(data.encode())

    conn.close()


if __name__ == '__main__':
    server()
