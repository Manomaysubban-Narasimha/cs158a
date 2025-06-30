# CS158A - Assignment 2: Multi-Client Chat

This project implements a multi-client chat application using Python's `socket` and `threading` libraries.

[cite_start]The system consists of a server (`mychatserver.py`) and one or more clients (`mychatclient.py`) that communicate over TCP sockets. [cite: 7]

## Code Description and Features

* **`mychatserver.py`**: The central server that listens for client connections.
    * [cite_start]It is multi-threaded, spawning a new thread for each connected client to handle communication. [cite: 8]
    * [cite_start]It maintains a list of all active clients. [cite: 2]
    * [cite_start]When it receives a message from a client, it broadcasts that message to all other connected clients. [cite: 2]
    * [cite_start]Messages are formatted with the sender's port number, e.g., `f"{port_number}: {message}"`. [cite: 6]

* **`mychatclient.py`**: The client program that users run to participate in the chat.
    * It uses two threads: one for sending user input and another for continuously receiving messages from the server. [cite_start]This allows for non-blocking communication. 
    * [cite_start]Users can type `exit` to disconnect gracefully from the server. [cite: 11]

## How to Run the Application

You will need at least two terminal windows: one for the server and one for each client you wish to connect.

### 1. Start the Server

In your first terminal, navigate to the `a2` directory and run the server script:

```bash
python mychatserver.py
```

You should see the following output, indicating the server is ready to accept connections:

```
[LISTENING] Server is listening on 127.0.0.1:12345
```

### 2. Start one or more Clients

In separate new terminals, navigate to the `a2` directory and run the client script. You can open as many client terminals as you like.

```bash
python mychatclient.py
```

[cite_start]Each client will connect to the server and display a welcome message. [cite: 15]

## [cite_start]Execution Example 

Here is an example of the output from the server and three clients, similar to the one in the assignment description.

**(This is a text-based representation. You should replace this with a screenshot or a copy-paste of your actual terminal output as required by the assignment instructions.)**

---

#### **Server Terminal**

```
[LISTENING] Server is listening on 127.0.0.1:12345
[NEW CONNECTION] ('127.0.0.1', 54321) connected.
[NEW CONNECTION] ('127.0.0.1', 54322) connected.
[NEW CONNECTION] ('127.0.0.1', 54323) connected.
[('127.0.0.1', 54321)] Relaying message: 54321: Hi everyone!
[('127.0.0.1', 54322)] Relaying message: 54322: Hello there!
[('127.0.0.1', 54323)] Relaying message: 54323: How is this chat assignment going?
[('127.0.0.1', 54321)] Relaying message: 54321: Pretty well, it seems to work!
[('127.0.0.1', 54322)] Sent exit command.
[DISCONNECTED] ('127.0.0.1', 54322) has been removed.
```

---

#### **Client 1 Terminal (Port 54321)**

```
Connected to chat server. Type 'exit' to leave.
Hi everyone!
54322: Hello there!
54323: How is this chat assignment going?
Pretty well, it seems to work!
exit
Disconnected from server
```

---

#### **Client 2 Terminal (Port 54322)**

```
Connected to chat server. Type 'exit' to leave.
54321: Hi everyone!
Hello there!
54323: How is this chat assignment going?
54321: Pretty well, it seems to work!
exit
Disconnected from server
```

---

#### **Client 3 Terminal (Port 54323)**

```
Connected to chat server. Type 'exit' to leave.
54321: Hi everyone!
54322: Hello there!
How is this chat assignment going?
54321: Pretty well, it seems to work!
exit
Disconnected from server
```