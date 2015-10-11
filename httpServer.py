from socket	import *
from sys import argv, exit

version = 0.2
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
	request = bytes.decode(request)
	return request

def parseRequest (request) :
	# dictionary to hold values
	details = {}
	# list of lines in request
	lines = request.split('\r\n')
	# components of line
	parts = lines[0].split(' ')
	details['type'] = parts[0].upper()
	details['file'] = parts[1]
	details['http'] = parts[2]

	# parts = lines[1].split(' ')
	# details['host'] = parts[1]

	# parts = lines[2].split(' ')
	# details['connection'] = parts[1]

	# parts = lines[3].split(' ')
	# details['accept'] = parts[1]

	# parts = lines[4].split(' ')
	# details['upgrade'] = parts[1]

	# parts = lines[5].split(' ')
	# details['agent'] = parts[1]

	# parts = lines[6].split(' ')
	# details['encoding'] = parts[1]

	# parts = lines[7].split(' ')
	# details['language'] = parts[1]

	print(details['type'] + ' ' + details['file'])
	return details

def getContent (details) :
	# process the request
	content = openFile(details['file'])
	return content

def returnResponse (response, socket) :
	# return the result to the client
	socket.send(response.encode("ascii"))

def listen () :
	while listening:
		# accept the connection to a client
		clientSocket, addr = serverSocket.accept()

		request = getRequest(clientSocket)

		details = parseRequest(request)

		response = getContent(details)

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
