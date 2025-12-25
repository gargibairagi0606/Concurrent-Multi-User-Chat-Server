import socket
import threading

HOST = '127.0.0.1'
PORT = 5693

def receive(sock):
    while True:
        try:
            print(sock.recv(1024).decode(), end="")
        except:
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    print(sock.recv(1024).decode(), end="")
    sock.send(input().encode())

    print(sock.recv(1024).decode(), end="")
    sock.send(input().encode())

    response = sock.recv(1024).decode()
    print(response)
    if "closed" in response.lower():
        sock.close()
        return

    threading.Thread(target=receive, args=(sock,), daemon=True).start()

    while True:
        msg = input()
        if msg.lower() == "exit":
            break
        sock.send(msg.encode())

    sock.close()

if __name__ == "__main__":
    main()
