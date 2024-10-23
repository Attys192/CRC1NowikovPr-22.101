import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
                
            else:
                break
        except:
            print("Произошла ошибка при получении сообщения.")
            break

def send_messages(client_socket):
    while True:
        message = input()
        if message == 'close':
            client_socket.send(message.encode('utf-8')) 
            print("Вы отключились от сервера.")
            client_socket.close()
            break
        client_socket.send(message.encode('utf-8'))

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("localhost", 12345)) 

    username = input("Введите ваше имя: ")
    client_socket.send(username.encode('utf-8'))  

    # Поток для получения сообщений
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.start()

    # Поток для отправки сообщений
    send_thread = threading.Thread(target=send_messages, args=(client_socket,))
    send_thread.start()


start_client()