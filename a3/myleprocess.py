# myleprocess.py
# CS 158A, Assignment 3: Leader Election

import socket
import threading
import time
import uuid
import json
import sys
import os

class Message:
    """Defines the structure for messages passed between nodes."""
    def __init__(self, sender_uuid, flag=0):
        self.uuid = str(sender_uuid)
        self.flag = flag

    def to_json(self):
        """Serializes the message instance to a JSON string."""
        return json.dumps(self.__dict__) + "\n"

    @staticmethod
    def from_json(json_str):
        """Deserializes a JSON string back into a Message instance."""
        data = json.loads(json_str)
        return Message(data['uuid'], data['flag'])


class Node:
    """Represents a process in the distributed system."""
    CONFIG_FILE = 'config.txt'
    CONNECTION_RETRY_DELAY = 10  # seconds

    def __init__(self, log_file_name):
        self.id = uuid.uuid4()
        self.log_file_name = log_file_name
        self.log_lock = threading.Lock()
        self.state_lock = threading.Lock()
        self.leader_id = None
        self.state = 0
        self.server_socket = None
        self.client_socket = None
        self.client_ready = threading.Event()
        self.shutdown_event = threading.Event()

        self.log(f"Node initialized with UUID: {self.id}")

        try:
            with open(self.CONFIG_FILE, 'r') as f:
                server_line = f.readline().strip().split(',')
                client_line = f.readline().strip().split(',')
                self.server_ip = server_line[0]
                self.server_port = int(server_line[1])
                self.neighbor_ip = client_line[0]
                self.neighbor_port = int(client_line[1])
        except (IOError, IndexError, ValueError) as e:
            self.log(f"FATAL: Error reading {self.CONFIG_FILE}: {e}")
            sys.exit(1)

    def log(self, message):
        """Writes a message to the node's log file in a thread-safe manner."""
        with self.log_lock:
            try:
                with open(self.log_file_name, 'a') as f:
                    f.write(f"[{time.ctime()}] {message}\n")
                print(message)
            except IOError as e:
                print(f"FATAL: Could not write to log file {self.log_file_name}: {e}")

    def start_server(self):
        """Initializes and runs the server functionality."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen(1)
        self.log(f"Server listening on {self.server_ip}:{self.server_port}")

        try:
            connection, address = self.server_socket.accept()
            self.log(f"Accepted connection from {address}")
            self.listen_for_messages(connection)
        except OSError:
            pass # Socket was closed
        finally:
            if 'connection' in locals(): connection.close()

    def connect_to_neighbor(self):
        """Initializes the client, retrying indefinitely until shutdown."""
        attempt = 0
        while not self.shutdown_event.is_set():
            try:
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.neighbor_ip, self.neighbor_port))
                self.log(f"Connected to neighbor at {self.neighbor_ip}:{self.neighbor_port}")
                self.client_ready.set()
                return
            except (ConnectionRefusedError, OSError):
                if self.shutdown_event.is_set(): break
                attempt += 1
                # self.log(f"Connection to neighbor refused. Retrying... (Attempt {attempt})")
                time.sleep(self.CONNECTION_RETRY_DELAY)

    def listen_for_messages(self, connection):
        """Listens for incoming messages from the neighbor."""
        self.log("Server thread waiting for client connection...")
        self.client_ready.wait()
        
        if self.client_socket:
            self.log("Client connected. Sending initial message.")
            self.send_message(Message(self.id))
        
        buffer = ""
        while not self.shutdown_event.is_set():
            try:
                connection.settimeout(1.0)
                data = connection.recv(1024).decode('utf-8')
                if not data: break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split('\n', 1)
                    msg = Message.from_json(line)
                    self.log_received(msg)
                    self.process_message(msg)
            except socket.timeout:
                continue
            except (json.JSONDecodeError, socket.error, OSError):
                break
        self.log("Ending listen loop.")

    def send_message(self, message):
        """Sends a message to the neighbor."""
        if not self.client_socket: return
        try:
            self.client_socket.sendall(message.to_json().encode('utf-8'))
            self.log_sent(message)
        except socket.error as e:
            self.log(f"Error sending message: {e}")

    def process_message(self, msg):
        """Implements the leader election logic."""
        msg_uuid = uuid.UUID(msg.uuid)
        with self.state_lock:
            if self.state == 1:
                # If the leader is known, announce it and ignore election messages
                self.log(f"Message ignored: Leader is already known to be {self.leader_id}")
                return
            
            if msg_uuid > self.id:
                self.send_message(msg)
            elif msg_uuid < self.id:
                self.log(f"Message ignored: Received UUID {msg_uuid} is smaller than my UUID {self.id}.")
            
            # This block is only reached when a node receives its own UUID back
            elif msg_uuid == self.id:
                self.log(f"LEADER: My own UUID {self.id} has returned. I am the leader.")
                self.leader_id = self.id
                self.state = 1
                self.log(f"leader is {self.leader_id}")
                # Announce leadership to the ring
                self.send_message(Message(self.id, flag=1))

    def log_received(self, msg):
        """Logs received messages, safely reading state."""
        comparison = "greater" if uuid.UUID(msg.uuid) > self.id else "less" if uuid.UUID(msg.uuid) < self.id else "same"
        with self.state_lock:
            current_state = self.state
            current_leader_id = self.leader_id
        
        log_msg = f"Received: uuid={msg.uuid}, flag={msg.flag}, {comparison}, state={current_state}"
        # Add leader_id to log if state is 1 
        if current_state == 1:
            log_msg += f", leader_id={current_leader_id}"
        self.log(log_msg)

    def log_sent(self, msg):
        """Logs sent messages."""
        self.log(f"Sent: uuid={msg.uuid}, flag={msg.flag}")

    def run(self):
        """Starts threads and waits for Ctrl+C to shut down."""
        threads = [
            threading.Thread(target=self.start_server),
            threading.Thread(target=self.connect_to_neighbor)
        ]
        
        for t in threads:
            t.start()

        try:
            while any(t.is_alive() for t in threads):
                time.sleep(1)
        except KeyboardInterrupt:
            self.log("Ctrl+C detected. Initiating shutdown...")
        finally:
            self.shutdown_event.set()
            self.log("Cleaning up resources...")
            if self.server_socket: self.server_socket.close()
            if self.client_socket: self.client_socket.close()
            for t in threads:
                t.join()
            self.log("Shutdown complete.")


def main():
    if len(sys.argv) != 2:
        print("Usage: python myleprocess.py <log_file_name>")
        sys.exit(1)
    
    log_file_path = sys.argv[1]
    if os.path.exists(log_file_path):
        os.remove(log_file_path)

    node = Node(log_file_path)
    node.run()


if __name__ == "__main__":
    main()