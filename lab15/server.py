import os
import socket

HOST = os.getenv("ECHO_SERVER_HOST", "")
PORT = int(os.getenv("ECHO_SERVER_PORT", "9090"))

sock = socket.socket()
print("Server is created, starting...")
sock.bind((HOST, PORT))
sock.listen(0)
print(f"Server is listening on IP {HOST} at port {PORT}")

conn, addr = sock.accept()
print(f"Connected client from address {addr[0]}, port {addr[1]}")

msg = ''

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(f"Receieved data from client {data}")
    msg += data.decode()
    conn.send(data)
    print(f"Echo data {data} is sent to client")

print(f"Client disconnected")

conn.close()

print(f"Server is shutting down. Thanks!")