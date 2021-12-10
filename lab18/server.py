import os
import socket
import threading
import datetime
import subprocess

HOST = os.getenv("ECHO_SERVER_HOST", "")
PORT = int(os.getenv("ECHO_SERVER_PORT", "9090"))


def ftp_ls(folder):
	files_list = subprocess.check_output(["ls", folder]).decode()
	return True, files_list

def ftp_mkdir(folder):
	try:
		output = subprocess.check_output(
			["mkdir", folder], stderr=subprocess.STDOUT, shell=True, timeout=3,
			universal_newlines=True)
	except subprocess.CalledProcessError as exc:
		return False, exc.output
	else:
		return True, ""

def ftp_rmdir(folder):
	try:
		output = subprocess.check_output(
			["rmdir", folder], stderr=subprocess.STDOUT, shell=True, timeout=3,
			universal_newlines=True)
	except subprocess.CalledProcessError as exc:
		return False, exc.output
	else:
		return True, ""

def ftp_rm(filename):
	try:
		output = subprocess.check_output(
			["rm", filename], stderr=subprocess.STDOUT, shell=True, timeout=3,
			universal_newlines=True)
	except subprocess.CalledProcessError as exc:
		return False, exc.output
	else:
		return True, ""

def ftp_mv(filename, new_filename):
	try:
		output = subprocess.check_output(
			["mv", filename, new_filename], stderr=subprocess.STDOUT, shell=True, timeout=3,
			universal_newlines=True)
	except subprocess.CalledProcessError as exc:
		return False, exc.output
	else:
		return True, ""

def ftp_upload(filename, data):
	try:
		with open(filename, "wb") as f:
			f.write(data)
	except Exception as exc:
		return False, exc.output
	else:
		return True, ""

def ftp_download(filename):
	try:
		with open(filename, "rb") as f:
			data = f.read()
			return True, data.decode()
	except Exception as exc:
		return False, exc.output


commands = {
	"LIST": ftp_ls,
	"MKD": ftp_mkdir,
	"RMD": ftp_rmdir,
	"DELE": ftp_rm,
	"RM": ftp_mv,
	"UPLOAD": ftp_upload,
	"DOWNLOAD": ftp_download
}

def process(msg):
	if not " " in msg:
		cmd, args = msg, ()
	else:
		cmd, args = msg.split(" ")[0], msg.split(" ")[1:]
	print(cmd, args)
	if cmd not in commands.keys():
		return "ERROR Command is not available"
	result, data = commands[cmd](*args)
	if result:
		return f"SUCCESS {data}"
	else:
		return f"ERROR {data}"


def new_client(conn, addr):
	
	print(f"[{datetime.datetime.now()}] Connected client from address {addr[0]}, port {addr[1]}")

	while True:
		data = conn.recv(1024**2)
		if not data:
			break
		msg = data.decode()

		print(msg)

		return_msg = process(msg)
		
		print(f"[{datetime.datetime.now()}] Receieved data from client {data}")
		conn.send(return_msg.encode())
		print(f"[{datetime.datetime.now()}] Echo data {return_msg} is sent to client")

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