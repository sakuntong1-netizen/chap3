import socket
import threading

# กำหนดค่าการเชื่อมต่อ
SERVER_HOST = 'server'  # ใช้ชื่อ service ของ server ใน Docker Compose
SERVER_PORT = 65432

def receive_messages(client):
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if not msg:
                break
            print(f"\nReceived: {msg}")
        except:
            print("Disconnected from server.")
            break

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER_HOST, SERVER_PORT))
    print("Connected to server.")
    threading.Thread(target=receive_messages, args=(client,)).start()
    while True:
        msg = input("Enter message: ")
        try:
            client.send(msg.encode('utf-8'))
        except:
            print("Error sending message.")
            break

if __name__ == "__main__":
    start_client()