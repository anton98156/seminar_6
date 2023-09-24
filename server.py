import socket
from threading import Thread

host = 'ENTER YOUR IP'
port = 55555

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((host, port))
server_socket.listen()

connected_clients = []
client_nicks = []

def send_message_to_all_clients(message):
    for client in connected_clients:
        client.send(message)

def client_handler(client_conn):
    while True:
        try:
            client_message = client_conn.recv(1024)
            send_message_to_all_clients(client_message)
        except:
            client_index = connected_clients.index(client_conn)
            connected_clients.remove(client_conn)
            client_conn.close()
            disconnected_nick = client_nicks[client_index]
            send_message_to_all_clients(f'{disconnected_nick} left!'.encode('ascii'))
            client_nicks.remove(disconnected_nick)
            break

def wait_for_connection():
    while True:
        client, addr = server_socket.accept()

        print(f"Connected with {str(addr)}")

        client.send('NICK'.encode('ascii'))
        nick_name = client.recv(1024).decode('ascii')
        client_nicks.append(nick_name)
        connected_clients.append(client)

        print(f'Nickname is {nick_name}')
        send_message_to_all_clients(f"{nick_name} joined!".encode('ascii'))
        client.send('You are connected to the server!'.encode('ascii'))

        Thread(target=client_handler, args=(client,)).start()

print("Server is listening...")
wait_for_connection()