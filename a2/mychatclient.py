import socket
import threading

# Configuration 
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
BUFSIZE = 1024      # Buffer size for receiving data, as per instructions, set to 1024 bytes.


def receive_messages(client_socket):
    """
    This function runs in a separate thread and continuously listens for
    messages from the server.
    """
    while True:
        try:
            # Wait to receive a message from the server.
            message = client_socket.recv(BUFSIZE)
            if not message:
                # If the message is empty, the server has closed the connection.
                print("\n[DISCONNECTED] Server connection lost.")
                break
            
            # Print the received message from the server.
            # The message is already formatted by the server as "port: message" 
            print(message.decode('utf-8'))

        except (ConnectionAbortedError, ConnectionResetError):
            # This handles the case where the connection is suddenly closed.
            print("\n[DISCONNECTED] Connection to the server has been closed.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


def send_messages(client_socket):
    """
    This function runs in the main thread and handles sending user input
    to the server.
    """
    print("Connected to chat server. Type 'exit' to leave.") 
    while True:
        try:
            # Wait for the user to type a message.
            message = input()

            # The user can type 'exit' to gracefully leave the chat 
            if message.strip().lower() == 'exit':
                client_socket.send(message.encode('utf-8')) # Send 'exit' to the server 
                break # Exit the loop to terminate the client

            # Send the raw text message to the server 
            client_socket.send(message.encode('utf-8'))
        
        except (EOFError, KeyboardInterrupt):
            # Handle Ctrl+D or Ctrl+C to gracefully exit
            print("\nExiting...")
            client_socket.send('exit'.encode('utf-8'))
            break
            
        except Exception as e:
            print(f"An error occurred while sending: {e}")
            break
            
    client_socket.close()
    print("Disconnected from server")


def start_client():
    """
    Main function to initialize and run the client.
    """
    # Create a TCP socket 
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"[ERROR] Connection refused. Is the server running on {HOST}:{PORT}?")
        return

    # Create and start a thread for receiving messages 
    # This allows the client to listen for incoming messages while the user is typing.
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True  # Allows main thread to exit even if this thread is running
    receive_thread.start()

    # The main thread will handle sending messages.
    send_messages(client_socket)


if __name__ == "__main__":
    start_client()