import socket
import threading

# Server connection details
SERVER_IP = "127.0.0.1"
SERVER_PORT = 12345
BUFFER_SIZE = 1024

# List to keep track of connected clients
clients = []

def handle_client(client_socket, client_address):
    """
    Handles communication with a connected client.
    """
    print(f"[NEW CONNECTION] {client_address} connected.")
    clients.append(client_socket)
    try:
        while True:
            message = client_socket.recv(BUFFER_SIZE)
            if not message:
                break
            broadcast_message(message, client_socket)
    except socket.error as e:
        print(f"[ERROR] Connection with {client_address} lost: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        print(f"[DISCONNECT] {client_address} disconnected.")

def broadcast_message(message, sender_socket):
    """
    Sends the received message to all connected clients except the sender.
    """
    for client in clients:
        if client != sender_socket:
            try:
                client.sendall(message)
            except socket.error as e:
                print(f"[ERROR] Could not send message to client: {e}")

def start_server():
    """
    Starts the server and listens for incoming client connections.
    """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen(5)
    print(f"[LISTENING] Server is listening on {SERVER_IP}:{SERVER_PORT}")

    try:
        while True:
            client_socket, client_address = server_socket.accept()
            client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
            client_handler.start()
    except KeyboardInterrupt:
        print("\n[SHUTDOWN] Server is shutting down.")
    finally:
        server_socket.close()

if __name__ == "__main__":
    print("[STARTING] Server is starting...")
    start_server()
