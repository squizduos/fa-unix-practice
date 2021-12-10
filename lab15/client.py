import os
import socket
from time import sleep

HOST = os.getenv("ECHO_SERVER_HOST", "127.0.0.1")
PORT = int(os.getenv("ECHO_SERVER_PORT", "9090"))

sock = socket.socket()
sock.setblocking(1)
print(f"Connecting to server {HOST}, port {PORT}")
sock.connect((HOST, PORT))
print(f"Connected successfully!")

msg = input()
sock.send(msg.encode())
print(f"Sent message {msg} to server.")

data = sock.recv(1024)
print(f"Recieved {len(data)} bytes from server.")


print(f"Disconnecting from server...!")
sock.close()
print(f"Disconnected successfully!")

print(data.decode())