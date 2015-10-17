from socket	import *
from sys import argv, exit
import os

path = os.path.dirname(os.path.abspath(__file__))

version = 0.3
listening = True
MAX_FILE_SIZE = 8192
endl = "\r\n"

class NonGetRequestException (Exception) :
    pass

class NotFoundException (Exception) :
	pass

class BadRequestException (Exception) :
	pass

class FileTypeNotSupportedException (Exception) :
	pass

class HTTPVersionNotSupportedException (Exception) :
	pass

def getPort () :
	if len(argv) != 2 :
		print("Usage requires exactly one command line argument! python3 httpServer <port>")
		exit()
	return int(argv[1])

def openFile (fileName) :
	# Supported files:
	# HTML (.html or .htm), text (.txt), or JPEG (.jpg or .jpeg)
	try:
		inputfile = open (fileName, 'r')
	except IOError:
		raise NotFoundException
	contents = inputfile.read()
	return contents

def getRequest (socket) :
	# receive the request
	request = socket.recv(MAX_FILE_SIZE)
	request = bytes.decode(request)
	print(request)
	return request

def parseRequest (request) :
	# dictionary to hold values
	details = {}
	try :

		# list of lines in request
		lines = request.split('\r\n')
		# components of line
		parts = lines[0].split(' ')
		details['type'] = parts[0].upper()
		if details['type'] != "GET" :
			raise NonGetRequestException
		if '/' == parts[1][0] :
			parts[1] = path + parts[1]
		else :
			parts[1] = path + '/' + parts[1]
		details['file'] = parts[1]
		details['http'] = parts[2]
		if details['http'] != "HTTP/1.1" :
			raise HTTPVersionNotSupportedException

	except IndexError :
		raise BadRequestException

	# print(details['type'] + ' ' + details['file'])
	return details

def getContent (details) :
	# process the request
	content = openFile(details['file'])
	return content

def getResponse (details) :
	response  = ""
	response += details["HTTP"] + " " + details["code"] + endl
	response += "Date: Sun, 26 Sep 2010 20:09:20 GMT\r\n"
	response += "Server: Apache/2.0.52 (CentOS)\r\n"
	response += "Last-Modified: Tue, 30 Oct 2007 17:00:02 GMT\r\n"
	response += "Accept-Ranges: bytes\r\n"
	response += "Content-Length: " + str(len(details["content"])) + endl
	response += "Keep-Alive: timeout=10, max=100\r\n"
	response += "Connection: Keep-Alive\r\n"
	response += "Content-Type: text/html; charset=ISO-8859-1\r\n"
	response += endl
	response += details["content"]
	return response

def returnResponse (response, socket) :
	# return the result to the client
	socket.send(response.encode())

def listen () :
	while listening:

		# accept the connection to a client
		clientSocket, addr = serverSocket.accept()

		# obtain the request through the wire
		request = getRequest(clientSocket)

		try :

			# parse the request
			requestDetails = parseRequest(request)

			responseDict = {}
			responseDict["HTTP"] = "HTTP/1.1"

			try :

				responseDict["content"] = getContent(requestDetails)
				responseDict["code"] = "200 OK"

			except NotFoundException :
				print("File not found")
				responseDict["content"] = "404 Not Found"
				responseDict["code"] = "404 Not Found"

			response = getResponse(responseDict)

			returnResponse(response, clientSocket)

		except NonGetRequestException :
			print("Server only accepts GET requests")

		except BadRequestException :
			print("Bad request")

		except HTTPVersionNotSupportedException :
			print("Server only supports HTTP/1.1")

		#close the connection
		clientSocket.close()

print('TastyTTP v' + str(version))

# define port number and socket
port = getPort()
serverSocket = socket(AF_INET, SOCK_STREAM)

# activate socket
serverSocket.bind(('localhost', port))
serverSocket.listen(1)

listen()
