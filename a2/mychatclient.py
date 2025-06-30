# mychatclient.py (Corrected Version)

import socket
import threading

# --- Configuration ---
HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 12345        # The port used by the server
BUFSIZE = 1024      # Buffer size for receiving data, as per instructions.

def receive_messages(client_socket):
    """
    This function runs in a separate thread and continuously listens for
    messages from the server.
    """
    while True:
        try:
            message = client_socket.recv(BUFSIZE)
            if not message:
                print("\n[DISCONNECTED] Server connection lost.")
                break
            
            print(message.decode('utf-8'))

        except OSError:
            # This error occurs when the socket is closed by the main thread
            # after typing 'exit'. It's an expected part of the shutdown process,
            # so we can break the loop silently.
            break
        except Exception as e:
            # This will catch any other unexpected errors.
            print(f"An unexpected error occurred: {e}")
            break

def send_messages(client_socket):
    """
    This function runs in the main thread and handles sending user input
    to the server.
    """
    print("Connected to chat server. Type 'exit' to leave.")
    while True:
        try:
            message = input()

            if message.strip().lower() == 'exit':
                client_socket.send(message.encode('utf-8'))
                break 

            client_socket.send(message.encode('utf-8'))
        
        except (EOFError, KeyboardInterrupt):
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
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
    except ConnectionRefusedError:
        print(f"[ERROR] Connection refused. Is the server running on {HOST}:{PORT}?")
        return

    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    send_messages(client_socket)


if __name__ == "__main__":
    start_client()