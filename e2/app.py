from flask import Flask, request, render_template_string
import socket

app = Flask(__name__)

# หน้าเว็บฟอร์ม
form_html = """
<!doctype html>
<title>Send Message</title>
<h1>Send a message to the socket server</h1>
<form method="post">
  <textarea name="message"></textarea><br>
  <input type="submit" value="Send">
</form>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        message = request.form['message']

        # ส่งข้อความไปยังเซิร์ฟเวอร์ socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect(('socket_server', 12345))  # เปลี่ยน 'socket_server' ให้ตรงกับชื่อ service ใน docker-compose
        client_socket.sendall(message.encode())

        # รับการตอบกลับจากเซิร์ฟเวอร์
        response = client_socket.recv(1024).decode()
        client_socket.close()

        return f"<h1>Message sent:</h1><p>{message}</p><h2>Response from server:</h2><p>{response}</p>"

    return form_html

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
