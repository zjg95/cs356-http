from socket	import *
from sys import argv, exit

version = 0.1
listening = True

def getPort () :
	if len(argv) != 2 :
		print("Usage requires exactly one argument! python3 httpServer <port>")
		exit()
	return int(argv[1])

def openFile (fileName) :
	try:
		inputfile = open (fileName, 'r')
	except IOError:
		return '404'
	contents = inputfile.read()
	return contents

def getRequest (socket) :
	# receive the request
	request = socket.recv(2048)
	print(request)
	return request

def parseRequest (request) :
	# get/post
	# file
	pass

def getContent (request) :
	# process the request
	content = openFile(request)
	return content

def returnResponse (response, socket) :
	# return the result to the client
	socket.send(response.encode("ascii"))

def listen () :
	while listening:
		# accept the connection to a client
		clientSocket, addr = serverSocket.accept()

		request = getRequest(clientSocket)

		response = getContent(request)

		returnResponse(response, clientSocket)

		#close the connection
		clientSocket.close()

print('http server v' + str(version))

# define port number and socket
port = getPort()
serverSocket = socket(AF_INET, SOCK_STREAM)

# activate socket
serverSocket.bind(('localhost', port))
serverSocket.listen(1)

listen()

print("Exiting")
