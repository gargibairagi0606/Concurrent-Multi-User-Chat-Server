import socket
import threading
import queue

HOST = '127.0.0.1'
PORT = 5693
MAX_QUEUE = 10

users = {
    "user1": "user1p",
    "user2": "user2p",
    "user3": "user3p",
    "user4": "user4p"
}

clients = {}
lock = threading.Lock()


def broadcast(msg, sender=None):
    with lock:
        for u, data in clients.items():
            if u != sender:
                try:
                    data['queue'].put_nowait(msg)
                except queue.Full:
                    print(f"[DROP] Queue full for {u}")


def private_message(sender, target, msg):
    with lock:
        if target not in clients:
            clients[sender]['queue'].put(f"[SERVER] User {target} not online.\n".encode())
            return
        try:
            clients[target]['queue'].put_nowait(f"[PRIVATE] {sender}: {msg}\n".encode())
        except queue.Full:
            print(f"[DROP] Private msg to {target}")


def handle_client(conn, addr):
    username = None
    try:
        conn.send(b"Enter username: ")
        username = conn.recv(1024).decode().strip()

        conn.send(b"Enter password: ")
        password = conn.recv(1024).decode().strip()

        with lock:
            if username not in users or users[username] != password:
                conn.send(b"Invalid credentials. Connection closed.\n")
                conn.close()
                return

            if username in clients:
                conn.send(b"Username already logged in. Connection closed.\n")
                conn.close()
                print(f"[DUPLICATE LOGIN] {username}")
                return

            clients[username] = {"conn": conn, "queue": queue.Queue(MAX_QUEUE)}

        print(f"[CONNECTED] {username} from {addr}")
        broadcast(f"{username} joined the chat.\n".encode(), username)
        conn.send(f"Welcome {username}! Type 'exit' to leave.\n".encode())

        def sender():
            while True:
                msg = clients[username]['queue'].get()
                try:
                    conn.send(msg)
                except:
                    break

        threading.Thread(target=sender, daemon=True).start()

        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode().strip()
            if msg.lower() == "exit":
                break

            if msg.startswith("@"):
                parts = msg.split(" ", 1)
                if len(parts) != 2:
                    clients[username]['queue'].put(b"[SERVER] Use: @username message\n")
                    continue
                private_message(username, parts[0][1:], parts[1])
            else:
                broadcast(f"{username}: {msg}\n".encode(), username)
                print(f"[MESSAGE] {username}: {msg}")

    finally:
        with lock:
            if username in clients and clients[username]['conn'] == conn:
                del clients[username]
                broadcast(f"{username} left the chat.\n".encode(), username)
                print(f"[DISCONNECTED] {username}")
        conn.close()


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("Chat server running...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()


if __name__ == "__main__":
    main()
