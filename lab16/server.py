import os
import socket
import threading
import datetime

HOST = os.getenv("ECHO_SERVER_HOST", "")
PORT = int(os.getenv("ECHO_SERVER_PORT", "9090"))


def new_client(conn, addr):
	
	print(f"[{datetime.datetime.now()}] Connected client from address {addr[0]}, port {addr[1]}")

	while True:
		data = conn.recv(1024**2)
		if not data:
			break
		print(f"[{datetime.datetime.now()}] Receieved data from client {data}")
		conn.send(data)
		print(f"[{datetime.datetime.now()}] Echo data {data} is sent to client")

	print(f"[{datetime.datetime.now()}] Client disconnected")

	conn.close()


def listen_for_clients(sock):
	while True:
		conn, addr = sock.accept()
		thread = threading.Thread(target=new_client, args=(conn, addr))
		print(f"Created thread with name {thread.name}, starting process...")
		thread.start()

if __name__ == "__main__":
	sock = socket.socket()
	print("Server is created, starting...")

	sock.bind((HOST, PORT))

	sock.listen(0)
	print(f"Server is listening on IP {HOST} at port {PORT}")

	listen_for_clients(sock)
 
	print(f"Server is shutting down. Thanks!")