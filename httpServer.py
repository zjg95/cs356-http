from socket	import *
from sys import argv, exit

version = 0.1
listening = True

def getPort () :
	if len(argv) != 2 :
		print("Usage requires exactly one argument! python3 httpServer <port>")
		exit()
	return int(argv[1])

def request () :
	# receive the request
	request = client.recv(2048)
	print(request)
	return request

def process (request) :
	# process the request
	content = request.upper()
	return content

def respond (response) :
	# return the result to the client
	client.send(response)

def listen () :
	while listening:
		# accept the connection to a client
		client, addr = socket.accept()

		respond(process(request()))

		#close the connection
		client.close()

print('http server v' + str(version))

# define port number and socket
port = getPort()
socket = socket(AF_INET, SOCK_STREAM)

# activate socket
socket.bind(('localhost', port))
socket.listen(1)

listen()

print("Exiting")
