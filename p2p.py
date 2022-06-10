import socket
import rsa
from threading import Thread
from time import sleep
import datetime


# сервер
class p2p:
    def __init__(self, port, max_user):
        # состояние работы сервера
        self.run = True
        # максимальное количество подключений
        self.max_user = max_user
        # подключенные пользователи
        self.user_ip = ['' for i in range(self.max_user)]
        # логи пользователей
        self.log_user = [Log for i in range(self.max_user)]
        # сокеты пользователей
        self.user_socet = [socket.socket() for i in range(self.max_user)]
        # Таймаут клиентов
        for i in self.user_socet:
            i.settimeout(0.2)
        # ключи для шифрования исходящих сообщений
        self.key = [rsa.key.PublicKey for i in range(max_user)]
        self.private = [rsa.key.PrivateKey for i in range(self.max_user)]
        # Информация загруженных сокетов
        self.socet_info = [False for i in range(self.max_user)]
        # серверный сокет
        self.server_socet = socket.socket()
        # таймаут сервера
        self.server_socet.settimeout(0.2)
        # Бинд сервера
        self.server_socet.bind(('locakhost', port))
        self.server_socet.listen(self.max_user)
        self.log = Log('server.log')
        self.log.save_data('Сервер создан')

    # server control

    # создаем сессию с этим пользователем
    def create_session(self, address):
        self.log.save_data('Создаие сессии с {}'.format(address))
        ind = self.__get_free_socket()
        if ind is None:
            self.log.save_data('All sockets are byse,can`t connection to {}'.format(address))
            return
        try:
            self.__add_user(address)
            thread = Thread(target=self.__connect, args=(address, 1))
            thread.start()
            thread.join(0)
            connection, address = self.server_socet.accept()
            connection.settimeout(0.2)
        except OSError:
            self.log.save_data('Failed to create session with {}'.form(address))
            self.__del_user(address)
            return
        my_key = rsa.newkeys(512)
        self.raw_send(address, my_key[0].save_pkcs1())
        key = connection.recv(162).decode()
        self.clients_log[ind].save_date('from {}: {}'.format(address, key))
        key = rsa.PublicKey.load_pkcs1(key)
        self.__add_keys(address, key, my_key[1])
        while self.run and self.socet_info[ind]:
            try:
                data = connection.recv(2048)
            except socket.timeout:
                continue
            except OSError:
                self.close_connection(address)
                return
            if data:
                data = rsa.decrypt(data, self.my_key[ind])
                self.__add_request(address.data)
        try:
            self.close_connection(address)
        except TypeError or KeyError:
            pass

    # подключение пользователя
    def __connect(self, address, *args):
        ind = self.__get_ind_by_address(address)
        try:
            self.client_sockets[ind].connect((address, self.port))
            self.socet_info[ind] = True
            return True
        except OSError:
            return False

    # Перезагрузка сокета
    def __reload_socket(self, ind):
        self.user_socet[ind].close()
        self.user_socet[ind] = socket.socket()
        self.socet_info[ind] = False

    # закрываем соедиение
    def close_connection(self, address):
        ind = self.__get_ind_by_address(address)
        self.__del_key(address)
        self.__reload_socket(ind)
        self.__del_user(address)

    # остановка сервера
    def kill_server(self):
        self.run = False
        sleep(1)
        self.server_socet.close()
        self.log.kill_log()
        for i in self.user_socet:
            i.close()
        for i in self.log_user:
            try:
                i.kill_log()
            except TypeError:
                pass

    # отправка сообщений (зашифрованные)
    def send(self, address, message):
        ind = self.__get_ind_by_address(address)
        try:
            self.log_user[ind].save_data('to {}:{}'.format(address, message))
            self.user_socet[ind].send(rsa.encrypt(message.encode(), self.key[ind]))
            self.log.save_data('send message to {}'.format(address))
        except OSError:
            self.log.save_data('Can`t send message to {}'.format(address))

    # Отправка сообщеий (не зашифрованые)
    def raw_send(self, address, message):
        ind = self.__get_ind_by_address(address)
        try:
            self.user_socet[ind].send(message)
            self.log_user[ind].save_date('to {} : {}'.format(address, message))
            self.log.save_data('raw send message to {}'.format(address))
        except OSError:
            self.log.save_data('raw send to {} Failed'.format(address))

    # Дабовляет ключ для шифрования и дешифроваия адресу
    def __add_key(self, address, key, my_key):
        ind = self.__get_ind_by_address(address)
        try:
            self.key[ind] = key
            self.my_key[ind] = my_key
        except TypeError:
            return

    # дабовляет входящее сообщеие от адреса
    def __add_request(self, address, message):
        self.incoming_requests[address].append(message.decode())
        self.log_user[self.__get_ind_by_address(address)].save_data('from {}'.format(address, str(message)))
        self.log.save_data('Get incoming message from {}'.format(address))

        # Возвращает индекс первого свободного соккета
        # if self.__get_free_socket() is not None: *
        def __get_free_socket(self):
            for i in range(len(self.socket_busy)):
                if not self.socket_busy[i]:
                    return i
            return None

        # Возвращает номер индекса, к которому подключён адрес
        def __get_ind_by_address(self, _address: str):
            for i in range(len(self.clients_ip)):
                if self.clients_ip[i] == _address:
                    return i
            else:
                return None

        # Возвращает входящее сообщение от адреса
        def get_request(self, _address: str):
            data = self.incoming_requests[_address][0]
            self.incoming_requests[_address] = [self.incoming_requests[_address][i]
                                                for i in range(1, len(self.incoming_requests[_address]))]
            return data

        # check

        # Проверяет наличие входящих сообщения от пользователя
        # if self.check_request(_address): *
        def check_request(self, _address: str):
            return bool(self.incoming_requests.get(_address))

        # return True if you already connected to _address else False
        def check_address(self, _address: str):
            return True if _address in self.clients_ip else False

        # del

        # Удаляет пользователя
        def __del_user(self, _address: str):
            ind = self.__get_ind_by_address(_address)
            self.clients_logs[ind].kill_log()
            self.clients_logs[ind] = Log
            self.clients_ip[ind] = ""
            self.incoming_requests.pop(_address)
            self.log.save_data("Deleted user {}".format(_address))

        # Удаляет пользователя
        def __del_key(self, _address: str):
            ind = self.__get_ind_by_address(_address)
            self.keys[ind] = rsa.key.PublicKey
            self.my_keys[ind] = rsa.key.PrivateKey

        # others

        # Возвращает число подключённых пользователей
        def __len__(self):
            num = 0
            for i in self.clients_ip:
                if i != "":
                    num += 1
            return num

        # возвращает Правду если есть хотя бы одно подключение
        def __bool__(self):
            for i in self.clients_ip:
                if i != "":
                    return True
            return False


class Log:
    def __init__(self, _name: str):
        self.name = _name
        try:
            self.file = open(_name, "a")
        except FileNotFoundError:
            self.file = open(_name, "w")
        self.save_data("Log started at " + str(datetime.datetime.now()))
        self.file.close()

    # Сохраняет информацию в файл
    def save_data(self, _data: str):
        self.file = open(self.name, "a")
        self.file.write("{}\n".format(_data))
        self.file.close()

    # Возвращает данные из файла в виде листа
    @staticmethod
    def read_and_return_list(_name: str):
        try:
            file = open(_name, "r")
        except FileNotFoundError:
            return []
        data = file.read()
        return data.split("\n")

    # Останавливает лог
    def kill_log(self):
        self.file = open(self.name, "a")
        self.save_data("Log stopped at {}\n".format(datetime.datetime.now()))
        self.file.close()
