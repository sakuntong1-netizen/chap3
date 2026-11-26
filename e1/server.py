import socket
import threading

# กำหนดค่าการเชื่อมต่อ
HOST = '0.0.0.0'
PORT = 65432

clients = []

def handle_client(conn, addr):
    print(f"Client {addr} connected.")
    while True:
        try:
            msg = conn.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"Message from {addr}: {msg}")
            broadcast(msg, conn)
        except:
            break
    print(f"Client {addr} disconnected.")
    clients.remove(conn)
    conn.close()

def broadcast(message, sender_conn):
    for client in clients:
        if client != sender_conn:
            try:
                client.send(message.encode('utf-8'))
            except:
                pass

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server started on {HOST}:{PORT}")
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start_server()
