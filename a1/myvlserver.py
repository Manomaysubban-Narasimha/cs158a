# myvlserver.py
# This server implements a TCP socket that handles variable-length messages
# using a length-prefix protocol. The first 2 bytes of each message indicate
# the length of the following message content.

from socket import *  # Import all socket-related functions and constants

def receive_full_message(cn_socket, bufsize):
    """
    Receives a message with a 2-byte length prefix.
    Keeps receiving data until the full message is received.
    
    Args:
        cn_socket: The client connection socket
        bufsize: Maximum size of each receive operation
        
    Returns:
        tuple: (decoded_message, message_length) or (None, None) if error
    """
    try:
        # Step 1: Receive the 2-byte length prefix
        # The length is sent as a 2-character string like "10" or "05"
        # This allows for messages up to 99 characters long
        msg_len_str = cn_socket.recv(2).decode()
        if not msg_len_str:
            return None, None  # Connection closed by client
        msg_len = int(msg_len_str)
        print(f"Length of message received: {msg_len}")

        # Step 2: Receive the complete message in chunks
        # This loop handles messages larger than the buffer size
        message_chunks = []
        bytes_received = 0
        while bytes_received < msg_len:
            # Calculate how many bytes to receive in this iteration
            # Either the remaining message length or the buffer size, whichever is smaller
            chunk = cn_socket.recv(min(msg_len - bytes_received, bufsize))
            if not chunk:
                # This would happen if the client disconnects mid-message
                raise ConnectionError("Client disconnected during message transfer.")
            message_chunks.append(chunk)
            bytes_received += len(chunk)
        
        # Step 3: Combine all chunks and decode the complete message
        full_message = b''.join(message_chunks).decode()
        print(f"processed: {full_message}")
        return full_message, msg_len

    except (ValueError, ConnectionError) as e:
        # Handle errors in message reception or decoding
        print(f"Error receiving message: {e}")
        return None, None


def handle_client(cn_socket, addr, bufsize):
    """
    Handles a single client connection: receive, process, send back.
    
    Args:
        cn_socket: The client connection socket
        addr: Tuple containing client's IP address and port
        bufsize: Maximum size of each receive operation
    """
    print(f"Connected from {addr[0]}:{addr[1]}")
    
    # Receive the variable-length message from the client
    received_message, msg_len = receive_full_message(cn_socket, bufsize)

    # Process and respond only if message was received successfully
    if received_message:
        # Convert the message to uppercase as per protocol requirements
        capitalized_message = received_message.upper()

        # Prepare response in the same format: 2-byte length + message
        # Format the length to be a 2-digit string with leading zero if needed
        # Example: 5 -> "05", 10 -> "10"
        response_len_str = f"{len(capitalized_message):02d}"
        response = response_len_str + capitalized_message
        
        # Send the complete response
        # sendall() ensures the entire message is sent, even if it's larger than the buffer
        cn_socket.sendall(response.encode())
        print(f"Length of message sent: {len(capitalized_message)}")
        print(f"Message sent: {capitalized_message}")

    print("Connection closed\n")
    cn_socket.close()


def main():
    """
    Main function to set up the server and listen for clients.
    Creates a TCP socket, binds it to a port, and continuously accepts client connections.
    """
    # Server configuration
    server_port = 12000  # Port number for the server
    bufsize = 64  # Maximum size of each receive operation, as required by assignment

    # Create and configure the server socket
    server_socket = socket(AF_INET, SOCK_STREAM)  # AF_INET for IPv4, SOCK_STREAM for TCP
    server_socket.bind(('', server_port))  # Bind to all available interfaces
    server_socket.listen(1)  # Allow one queued connection
    
    print("The server is ready to receive messages")

    # Main server loop
    # This loop allows the server to handle multiple clients sequentially
    # Each client is handled completely before moving to the next
    while True:
        # Wait for and accept a new client connection
        connection_socket, addr = server_socket.accept()
        # Handle the client's request
        handle_client(connection_socket, addr, bufsize)


if __name__ == "__main__":
    main()