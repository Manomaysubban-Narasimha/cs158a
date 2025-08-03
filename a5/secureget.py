import socket
import ssl

def make_secure_request(host, port):
    """
    Establishes a secure connection to a host, sends an HTTP GET request for the
    root path, and returns the server's full response.

    Args:
        host (str): The server hostname (e.g., 'www.google.com').
        port (int): The port to connect to (e.g., 443 for HTTPS).

    Returns:
        bytes: The complete HTTP response from the server, or None on failure.
    """
    try:
        # Create a standard TCP socket and wrap it with SSL
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context()
        secure_sock = context.wrap_socket(sock, server_hostname=host)

        # Connect and send the request
        print(f"Connecting to {host} on port {port}...")
        secure_sock.connect((host, port))
        print("Connection successful.")

        request = b"GET / HTTP/1.1\r\nHost: " + host.encode() + b"\r\nConnection: close\r\n\r\n"
        print("Sending HTTP GET request...")
        secure_sock.sendall(request)

        # Receive the full response
        response = b""
        while True:
            data = secure_sock.recv(4096)
            if not data:
                break
            response += data
        
        print("Response received.")
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        return None
    finally:
        # Ensure the socket is always closed
        if 'secure_sock' in locals():
            secure_sock.close()
            print("Connection closed.")


def save_html_content(response_data, filename):
    """
    Parses a raw HTTP response, extracts the HTML content, and saves it to a file.

    Args:
        response_data (bytes): The raw HTTP response.
        filename (str): The name of the file to save the HTML to.
    """
    if not response_data:
        print("No response data to save.")
        return

    try:
        # The HTML body starts after the first double newline characters (\r\n\r\n)
        header_end = response_data.find(b"\r\n\r\n")
        if header_end != -1:
            # The HTML starts 4 bytes after the header separator
            html_content = response_data[header_end + 4:]
            with open(filename, 'wb') as f:
                f.write(html_content)
            print(f"Successfully saved HTML content to {filename}.")
        else:
            print("Could not find the end of the HTTP headers.")
    except Exception as e:
        print(f"Could not save file: {e}")


def main():
    """
    Main function to execute the secure web request.
    """
    HOST = 'www.google.com'
    PORT = 443
    FILENAME = 'response.html'

    # Make the request and get the response
    full_response = make_secure_request(HOST, PORT)

    # Save the HTML content from the response
    save_html_content(full_response, FILENAME)


if __name__ == "__main__":
    main()