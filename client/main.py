import time
import socket
import threading

thread_vector = []

class tThread(threading.Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.runing = True

    def run(self):
        while self.runing:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            client_socket.settimeout(1.0)
            message = bytes('Software ' + str(self.name), encoding='utf-8')
            addr = ("127.0.0.1", 12000)
            start = time.time()
            client_socket.sendto(message, addr)
            time.sleep(1)
            try:
                data, server = client_socket.recvfrom(1024)
                end = time.time()
                elapsed = end - start
            except socket.timeout:
                print(f'REQUEST TIMED OUT')

if __name__ == "__main__":
    while True:
        user_input = input()
        if user_input == 'exit':
            break
        else:
            if user_input.startswith("create "):
                name = str(user_input.split("create")[1])
                thread_name = name.strip()
                t = tThread(name=name)
                t.start()
                thread_vector.append(t)

            elif user_input.startswith("stop "):
                index = int(user_input.split("stop")[1])
                thread_vector[index -1].runing = False

            elif user_input.startswith("show"):
                print(thread_vector)

            else:
                print('Comando Inválido.')

            

