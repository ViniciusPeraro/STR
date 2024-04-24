import time
import socket
import threading

def sendMessage(prgName):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(1.0)
    message = bytes('Software ' + str(prgName), encoding='utf-8')
    addr = ("127.0.0.1", 12000)

    start = time.time()
    client_socket.sendto(message, addr)
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
            if user_input.startswith("p"):
                valor_p = str(user_input.split("p")[1])
                t = threading.Thread(target=sendMessage, args=(valor_p))
                t.start()