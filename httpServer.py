from socket	import *
from sys import argv, exit
import os

path = os.path.dirname(os.path.abspath(__file__))

version = 0.2
listening = True
MAX_FILE_SIZE = 8192

class HTTPException (Exception) :
    pass

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
	request = socket.recv(MAX_FILE_SIZE)
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
	if details['type'] != "GET" :
		raise HTTPException
	if '/' == parts[1][0] :
		parts[1] = path + parts[1]
	else :
		parts[1] = path + '/' + parts[1]
	details['file'] = parts[1]
	details['http'] = parts[2]

	print(details['type'] + ' ' + details['file'])
	return details

def getContent (details) :
	# process the request
	content = openFile(details['file'])
	return content

def getResponse (content) :
	response  = "HTTP/1.1 200 OK\r\n"
	response += "Date: Sun, 26 Sep 2010 20:09:20 GMT\r\n"
	response += "Server: Apache/2.0.52 (CentOS)\r\n"
	response += "Last-Modified: Tue, 30 Oct 2007 17:00:02 GMT\r\n"
	response += "Accept-Ranges: bytes\r\n"
	response += "Content-Length:" + str(len(content)) + "\r\n"
	response += "Keep-Alive: timeout=10, max=100\r\n"
	response += "Connection: Keep-Alive\r\n"
	response += "Content-Type: text/html; charset=ISO-8859-1\r\n"
	response += "\r\n"
	response += content
	return response

def returnResponse (response, socket) :
	# return the result to the client
	socket.send(response.encode("ascii"))

def listen () :
	while listening:
		# accept the connection to a client
		clientSocket, addr = serverSocket.accept()

		request = getRequest(clientSocket)

		try :

			requestDetails = parseRequest(request)

			content = getContent(requestDetails)

			response = getResponse(content)

			returnResponse(response, clientSocket)

		except :
			print("Server only accepts GET requests")

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
