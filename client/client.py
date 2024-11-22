import socket

def start_client(host='localhost', port=12345):
    # Create a TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")
    
    try:
        while True:
            # Input a message to send to the server
            message = input("Enter message (type 'exit' to quit): ")
            if message.lower() == 'exit':
                print("Closing connection.")
                break
            
            # Send the message to the server
            client_socket.send(message.encode('utf-8'))
            
            # Receive a response from the server
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Server response: {response}")
    finally:
        # Close the socket when done
        client_socket.close()

# Run the client
if __name__ == "__main__":
    start_client()
