import socket
import threading

# Configuration 
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on (non-privileged ports are > 1023)
BUFSIZE = 1024      # Buffer size for receiving data, as per instructions, set to 1024 bytes.


#  State 
#  the socket object will be stored for each connected client.
clients = []
# Lock is used to prevent race conditions when multiple threads
# try to modify the clients list at the same time.
clients_lock = threading.Lock()

def broadcast(message, sender_conn):
    """
    Sends a message to all connected clients except the sender.
    """
    with clients_lock:
        for client_conn in clients:
            # Don't send the message back to the original sender 
            if client_conn != sender_conn:
                try:
                    client_conn.send(message)
                except socket.error:
                    # If sending fails, assume the client has disconnected.
                    # Will remove them in the handle_client function.
                    pass


def handle_client(conn, addr):
    """
    This function runs in a dedicated thread for each connected client. 
    It handles receiving messages from a client and broadcasting them.
    """
    print(f"[NEW CONNECTION] {addr} connected.")
    client_port = addr[1] # Get the client's port number

    with clients_lock:
        clients.append(conn)

    try:
        while True:
            # Wait to receive a message from the client.
            message = conn.recv(BUFSIZE)
            if not message:
                # If recv returns an empty bytes object, the client has disconnected.
                break

            decoded_message = message.decode('utf-8')

            # Handle the 'exit' command from a client 
            if decoded_message.strip().lower() == 'exit':
                print(f"[{addr}] Sent exit command.")
                break

            # Format the message to include the sender's port number 
            # This is the format required for other clients to see.
            formatted_message = f"{client_port}: {decoded_message}".encode('utf-8')
            print(f"[{addr}] Relaying message: {formatted_message.decode('utf-8')}")

            # Broadcast the message to all other clients
            broadcast(formatted_message, conn)

    except ConnectionResetError:
        print(f"[CONNECTION LOST] {addr} disconnected unexpectedly.")
    finally:
        # This block executes whether the client typed 'exit' or disconnected abruptly.
        # It ensures the client is properly removed from the server's list.
        print(f"[DISCONNECTED] {addr} has been removed.")
        with clients_lock:
            if conn in clients:
                clients.remove(conn)
        conn.close()


def start_server():
    """
    The main function to start the chat server.
    """
    # Create a TCP socket 
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print(f"[LISTENING] Server is listening on {HOST}:{PORT}")

    # The server waits for new clients indefinitely until manually stopped 
    while True:
        # Accept a new connection. This is a blocking call.
        conn, addr = server_socket.accept()

        # Create a new thread to handle this client.
        # This allows the server to handle multiple clients simultaneously.
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start() # Start the thread's activity 


if __name__ == "__main__":
    start_server()