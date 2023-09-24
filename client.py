import socket
from threading import Thread

nick = input("Enter your nickname: ")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('ENTER YOUR IP SERVER ADDRESS', 55555))

def listen_to_server():
    while True:
        try:
            server_message = client_socket.recv(1024).decode('ascii')
            if server_message == 'NICK':
                client_socket.send(nick.encode('ascii'))
            else:
                print(server_message)
        except:
            print("An error occurred, closing connection.")
            client_socket.close()
            break

def chat():
    while True:
        message = f'{nick}: {input("")}'
        client_socket.send(message.encode('ascii'))

Thread(target=listen_to_server).start()
Thread(target=chat).start()