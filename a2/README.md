# CS158A - Assignment 2: Multi-Client Chat

This project implements a multi-client chat application using Python's `socket` and `threading` libraries.

The system consists of a server (`mychatserver.py`) and one or more clients (`mychatclient.py`) that communicate over TCP sockets. 

## Code Description and Features

* **`mychatserver.py`**: The central server that listens for client connections.
    * It is multi-threaded, spawning a new thread for each connected client to handle communication. 
    * It maintains a list of all active clients. 
    * When it receives a message from a client, it broadcasts that message to all other connected clients. 
    * Messages are formatted with the sender's port number, e.g., `f"{port_number}: {message}"`. 

* **`mychatclient.py`**: The client program that users run to participate in the chat.
    * It uses two threads: one for sending user input and another for continuously receiving messages from the server. This allows for non-blocking communication. 
    * Users can type `exit` to disconnect gracefully from the server. 

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

Each client will connect to the server and display a welcome message. 

## Execution Example 

Here is an example of the output from the server and three clients.

---

#### **Server Terminal**

```
[LISTENING] Server is listening on 127.0.0.1:12345
[NEW CONNECTION] ('127.0.0.1', 51839) connected.
[NEW CONNECTION] ('127.0.0.1', 51840) connected.
[NEW CONNECTION] ('127.0.0.1', 51843) connected.
[('127.0.0.1', 51839)] Relaying message: 51839: Hello, everyone!
[('127.0.0.1', 51840)] Relaying message: 51840: Hey!
[('127.0.0.1', 51843)] Relaying message: 51843: Wassup yall
[('127.0.0.1', 51839)] Relaying message: 51839: How are you all doing?
[('127.0.0.1', 51840)] Relaying message: 51840: I am doing well. What about yall?
[('127.0.0.1', 51843)] Relaying message: 51843: I am doing well. Have yall started studying for the exam yet?
[('127.0.0.1', 51839)] Relaying message: 51839: Nah not yet
[('127.0.0.1', 51840)] Relaying message: 51840: Me neither
[('127.0.0.1', 51843)] Relaying message: 51843: Yall wanna plan a study session tomorrow?
[('127.0.0.1', 51840)] Relaying message: 51840: Yea sure im down
[('127.0.0.1', 51839)] Relaying message: 51839: Ye me too
[('127.0.0.1', 51843)] Relaying message: 51843: Aight bet
[('127.0.0.1', 51843)] Relaying message: 51843: Let's meet up at the library at noon tomorrow, have lunch and get started reviewing
[('127.0.0.1', 51840)] Relaying message: 51840: Sounds good
[('127.0.0.1', 51839)] Relaying message: 51839: Looking forward to it! See yall tomorrow!
[('127.0.0.1', 51840)] Relaying message: 51840: Bet
[('127.0.0.1', 51839)] Sent exit command.
[DISCONNECTED] ('127.0.0.1', 51839) has been removed.
[('127.0.0.1', 51840)] Sent exit command.
[DISCONNECTED] ('127.0.0.1', 51840) has been removed.
[('127.0.0.1', 51843)] Sent exit command.
[DISCONNECTED] ('127.0.0.1', 51843) has been removed.
```

---

#### **Client 1 Terminal (Port 51839)**

```
Connected to chat server. Type 'exit' to leave.
Hello, everyone!
51840: Hey!
51843: Wassup yall
How are you all doing?
51840: I am doing well. What about yall?
51843: I am doing well. Have yall started studying for the exam yet?
Nah not yet
51840: Me neither
51843: Yall wanna plan a study session tomorrow?
51840: Yea sure im down
Ye me too
51843: Aight bet
51843: Let's meet up at the library at noon tomorrow, have lunch and get started reviewing
51840: Sounds good
Looking forward to it! See yall tomorrow!
51840: Bet
exit
An error occurred: [Errno 9] Bad file descriptor
Disconnected from server
```

---

#### **Client 2 Terminal (Port 51840)**

```
Connected to chat server. Type 'exit' to leave.
51839: Hello, everyone!
Hey!                  
51843: Wassup yall
51839: How are you all doing?
I am doing well. What about yall?
51843: I am doing well. Have yall started studying for the exam yet?
51839: Nah not yet
Me neither
51843: Yall wanna plan a study session tomorrow?
Yea sure im down
51839: Ye me too
51843: Aight bet
51843: Let's meet up at the library at noon tomorrow, have lunch and get started reviewing
Sounds good
51839: Looking forward to it! See yall tomorrow!
Bet
exit
An error occurred: [Errno 9] Bad file descriptor
Disconnected from server
```

---

#### **Client 3 Terminal (Port 51843)**

```
Connected to chat server. Type 'exit' to leave.
51839: Hello, everyone!
51840: Hey!
Wassup yall
51839: How are you all doing?
51840: I am doing well. What about yall?
I am doing well. Have yall started studying for the exam yet?
51839: Nah not yet
51840: Me neither
Yall wanna plan a study session tomorrow?
51840: Yea sure im down
51839: Ye me too
Aight bet
Let's meet up at the library at noon tomorrow, have lunch and get started reviewing
51840: Sounds good
51839: Looking forward to it! See yall tomorrow!
51840: Bet
exit
An error occurred: [Errno 9] Bad file descriptor
Disconnected from server
```