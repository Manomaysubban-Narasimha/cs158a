# Assignment 1: Variable-Length Messages

This project contains a Python client and server that communicate over TCP sockets. They use a simple protocol to handle messages of arbitrary length. The message is prefixed with a 2-byte number indicating its length.

## Cloning the Repository

To get a local copy of this project for development or testing, open your terminal and navigate to your preferred directory for cloning the repository and run the following git command:

```bash
git clone https://github.com/Manomaysubban-Narasimha/cs158a.git
```

## How to Run

After cloning the repository, follow these steps:

1. Open two separate terminal windows
2. Navigate to the cs158a/a1 directory in both terminals:
   ```bash
   cd cs158a/a1
   ```
3. In the first terminal, start the server:
   ```bash
   python myvlserver.py
   ```
4. In the second terminal, run the client:
   ```bash
   python myvlclient.py
   ```

The client will prompt you for input. Enter a message prefixed with its two-digit length where the length corresponds to the total number of characters that form the message (e.g., `10helloworld`).

## Execution Example

Here is an example of the output from the client and server terminals:

### Client Side
```
Input lowercase sentence: 99The 5 quick brown foxes jump over the 13 lazy dogs! This is a 99-character test for CS158a sockets.
From Server: THE 5 QUICK BROWN FOXES JUMP OVER THE 13 LAZY DOGS! THIS IS A 99-CHARACTER TEST FOR CS158A SOCKETS.
```

### Server Side
```
The server is ready to receive messages
Connected from 127.0.0.1:62835
Length of message received: 99
processed: The 5 quick brown foxes jump over the 13 lazy dogs! This is a 99-character test for CS158a sockets.
Length of message sent: 99
Message sent: THE 5 QUICK BROWN FOXES JUMP OVER THE 13 LAZY DOGS! THIS IS A 99-CHARACTER TEST FOR CS158A SOCKETS.
Connection closed
