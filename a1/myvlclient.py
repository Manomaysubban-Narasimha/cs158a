# myvlclient.py
# This client implements a TCP socket that sends variable-length messages to the server
# and receives responses. It uses the same length-prefix protocol as the server,
# where the first 2 bytes indicate the length of the following message.

from socket import *  

def receive_full_response(client_socket, bufsize):
    """
    Receives a response with a 2-byte length prefix from the server.
    Handles the complete message reception process, including chunking for large messages.
    
    Args:
        client_socket: The socket connected to the server
        bufsize: Maximum size of each receive operation
        
    Returns:
        str: The decoded response message, or None if an error occurs
    """
    try:
        # Step 1: Receive the 2-byte length prefix for the server's response
        # The length is sent as a 2-character string like "10" or "05"
        response_len_str = client_socket.recv(2).decode()
        if not response_len_str:
            return None  # Server closed the connection
        try:
            response_len = int(response_len_str)
        except ValueError:
            print(f"Error: Could not convert received length '{response_len_str}' to integer because length is not provided.")
            return None # Server closed the connection

        # Step 2: Receive the complete message in chunks
        # This loop handles responses larger than the buffer size
        message_chunks = []
        bytes_received = 0
        while bytes_received < response_len:
            # Calculate how many bytes to receive in this iteration
            # Either the remaining message length or the buffer size, whichever is smaller
            chunk = client_socket.recv(min(response_len - bytes_received, bufsize))
            if not chunk:
                raise ConnectionError("Server disconnected during message transfer.")
            message_chunks.append(chunk)
            bytes_received += len(chunk)
        
        # Step 3: Combine all chunks and decode the complete message
        return b''.join(message_chunks).decode()

    except (ValueError, ConnectionError) as e:
        # Handle errors in message reception or decoding
        print(f"Error receiving response: {e}")
        return None


def main():
    """
    Main function to set up the client, send a message, and receive the response.
    The client connects to the server, sends a single message, and then terminates.
    """
    # Server configuration
    server_name = 'localhost'  # Server is running on the same machine
    server_port = 12000       # Must match the server's port
    bufsize = 64             # Maximum size of each receive operation, as required by assignment

    # Create and connect the socket
    client_socket = socket(AF_INET, SOCK_STREAM)  # AF_INET for IPv4, SOCK_STREAM for TCP
    client_socket.connect((server_name, server_port))

    # Get user input
    # The user must provide the length manually as part of the input
    # Format: [length][message]
    # Example: "10helloworld" means "send 'helloworld' which is 10 characters long"
    sentence = input('Input lowercase sentence: ')

    # Send the complete message to the server
    # sendall() ensures the entire message is sent, even if it's larger than the buffer
    client_socket.sendall(sentence.encode())

    # Receive and process the server's response
    # The response will be the same message in uppercase
    modified_sentence = receive_full_response(client_socket, bufsize)

    # Display the response if received successfully
    if modified_sentence:
        print('From Server:', modified_sentence)

    # Clean up: close the socket and terminate
    # The client terminates after a single exchange is complete
    client_socket.close()


if __name__ == "__main__":
    main()