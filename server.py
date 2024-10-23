import socket
import threading

clients = []  

def handle_client(client_socket, client_address):

    username = client_socket.recv(1024).decode('utf-8')
    welcome_message = f"{username} подключился к чату!"
    transl(welcome_message, client_socket)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            transl(f"{username}: {message}", client_socket)
        
            
        except:
            break

    clients.remove(client_socket)
    
    transl(f"{username} покинул чат.", client_socket)

def transl(message, sender_socket=None):
    print(message)  
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("localhost", 12345))
    server_socket.listen()
    print("Сервер запущен.")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Подключен {client_address}.")
        clients.append(client_socket)
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()


start_server()