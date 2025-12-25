# Concurrent-Multi-User-Chat-Server
This project implements a concurrent TCP-based multi-user chat server in Python.
It demonstrates how multiple clients can communicate in real time using socket programming and multi-threading, while simulating flow-control and congestion-control behaviour.
The system supports:    
- Multiple clients connecting simultaneously    
- User authentication    
- Message broadcasting    
- Private messaging    
- Artificial flow and congestion control using message queues

## Scope of the Experiment
The objective of this experiment is to understand how concurrent network applications are designed and implemented at the socket level. The project focuses on:    
- TCP client–server communication    
- Multi-threaded server design    
- Handling multiple clients concurrently    
- Simulating flow control and congestion using bounded queues    
- Implementing basic user authentication and private messaging    

Advanced production-level features such as encrypted authentication, databases, or secure session handling are intentionally excluded in order to keep the implementation simple and aligned with academic learning objectives.

## How the Application Works
**Server Behavior**
- The server listens on a fixed TCP port.    
- Each incoming client connection is handled in a separate thread.    
- Clients are authenticated using predefined credentials.    
- For every connected client:
  - A dedicated message queue is maintained.    
  - Messages are broadcast to all other users.    
  - Queue size limits simulate congestion.    
- If a client disconnects or types exit, the server notifies all other users.    

**Client Behavior**
- The client connects to the server using TCP.    
- The user is prompted for a username and password.    
- After successful login:    
  - Messages typed by the user are sent to the server.    
  - Incoming messages are displayed in real time.    
- Typing exit cleanly disconnects the client.    

## Flow and Congestion Control
To simulate real network conditions:    
- Each client has a bounded message queue.    
- If a queue is full, messages are dropped.    
- Artificial delays are added while sending messages to simulate flow-control behaviour between fast and slow clients.    

## Authentication Note

For the purpose of this experiment, user credentials are stored directly within the server code using an in-memory data structure.    
This approach is intentionally chosen to keep the implementation simple and focused on understanding core networking concepts such as socket communication, concurrency, flow control, and message handling.    

In real-world applications, authentication is typically handled using secure databases and encryption mechanisms. However, those aspects are beyond the scope of this experiment and are therefore not included.    

## Project Structure

```
multi-user-chat-server/
├── client.py
├── server.py
├── README.md
└── .gitignore
```

## How to Run
**Start the Server**

```bash
python src/server.py
```

**Start the Client**
Open another terminal:

```bash
python src/client.py
```

## Commands
- Type any message to broadcast it.

- Private message format:    
```css
@username message
```
 Example:
```sql
@user2 Hello, how are you?
```
- To exit the chat:
```bash
exit
```

## Example Output
**Server**
```less
[CONNECTED] user1 from ('127.0.0.1', 62540)
[MESSAGE] user1: Hello everyone
```

**Client**
```pgsql
Welcome user1! Type 'exit' to leave.
user2 joined the chat.
user3: Hello everyone
```

## Key Concepts Demonstrated
- TCP socket programming in Python
- Multi-threaded server architecture
- Client authentication
- Flow and congestion control simulation
- Message broadcasting and private messaging
- Real-time distributed communication
