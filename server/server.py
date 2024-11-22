import socket

def start_server(host='localhost', port=12345):
    # Create a TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the specified host and port
    server_socket.bind((host, port))
    print(f"Server started and listening on {host}:{port}")
    
    # Listen for incoming connections
    server_socket.listen()
    
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f"Connection established with {client_address}")
        
        # Handle client communication
        while True:
            try:
                # Receive data from the client
                message = client_socket.recv(1024).decode('utf-8')
                if not message:
                    break
                print(f"Received from {client_address}: {message}")
                
                # Optionally, send a response back to the client
                client_socket.send("Message received!".encode('utf-8'))
            except ConnectionResetError:
                print(f"Connection lost with {client_address}")
                break

        # Close the client socket when done
        client_socket.close()
        print(f"Connection closed with {client_address}")

# Run the server
if __name__ == "__main__":
    start_server()