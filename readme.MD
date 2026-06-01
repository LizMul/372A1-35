# TCP Client-Server Application

## Description

A TCP-based client-server application developed using Python Socket API.

## Features

- User Login
- Message Transfer
- File Transfer
- Graceful Disconnect

## Requirements

- Python 3.x

## Project Structure

project/
├── server.py
├── client.py
├── users.txt
├── received_files/
├── README.md
└── protocol_documentation.pdf

## Running the Server

```bash
python server.py
```

The server starts listening on the configured IP and port.

## Running the Client

```bash
python client.py
```

Enter the server IP and port when prompted.

## Supported Commands

- `LOGIN Alice`
- `MSG Hello Server`
- `FILE test.txt`
- `QUIT`

## Example Session

```text
LOGIN Alice
MSG Hello
FILE report.pdf
QUIT
```

## Dependencies

- socket
- os
- json
- hashlib
- time

## Error Handling

The application handles:

- Invalid commands
- Missing files
- Empty messages
- Unexpected disconnects
- Invalid login attempts

## Protocol Documentation

### System overview

This application uses Python sockets to construct a TCP-based client-server architecture. Using a unique application-layer protocol, the client establishes a connection with the server and communicates with it. The protocol enables user login, text messaging, file transfer, and graceful disconnection.

### Protocol specification

This protocol is text-based. Every command starts with a keyword and then the necessary parameters. The supported commands are:

- `LOGIN`: Identify client/user (using an external file that lists valid users)
- `MSG`: Send text messages
- `FILE`: Transfer files
- `QUIT`: Terminate connection

### Command descriptions

- `LOGIN`
  - Syntax: `LOGIN: <username>`
  - Example: `LOGIN: Alice`
  - Server Response: `OK: Login Successful` or `ERROR: Invalid User`

- `MSG`
  - Syntax: `MSG: <message>`
  - Example: `MSG: Hello`
  - Server Response: `ACK: Message Received`

- `FILE`
  - Syntax: `FILE: <filename>:<filesize>`
  - Example: `FILE: assignment.pdf:1000`
  - Server Response: `READY`
  - Client sends file bytes after `READY` is received. When done: `ACK: File received`

- `QUIT`
  - Syntax: `QUIT`
  - Server Response: `BYE`
  - Connection is closed

### Message structure

Each message is a line of text sent over the TCP connection. Commands and parameters are separated by a colon (`:`). The server processes each request and replies with a status line.

### File transfer workflow

1. Client sends `FILE: <filename>:<filesize>`.
2. Server responds with `READY` if it can receive the file.
3. Client sends the raw file bytes.
4. Server writes the received bytes to `received_files/<filename>`.
5. Server responds with `ACK: File received`.

### Error handling rules

- Invalid commands receive an error response.
- Missing files are reported by the client before attempting transfer.
- Empty messages are rejected.
- Unexpected disconnects are handled without crashing.
- Incorrect protocol formats receive an error response.

### Connection termination procedure

The client sends `QUIT` to notify the server. The server responds with `BYE`, then closes the socket gracefully.