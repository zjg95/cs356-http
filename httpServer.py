from socket	import *
from sys import argv, exit
import os
import time

path = os.path.dirname(os.path.abspath(__file__))

serverName = "TastyTTP"
serverVersion = "1.0"
listening = True
MAX_FILE_SIZE = 8192
endl = "\r\n"
codeDict = {
	200 : "200 OK",
	400 : "400 Bad Request",
	403 : "403 Forbidden",
	404 : "404 Not Found",
	505 : "505 HTTP Version Not Supported"
}

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

def getCurrentTime () :
	return time.gmtime()

def getCurrentTimeString () :
	tnow = getCurrentTime()
	return time.strftime('%a, %d %b %Y %H:%M:%S GMT', tnow)

def getModifiedTime (fileName) :
	modtime = os.path.getmtime(fileName)
	return time.gmtime(modtime)

def getModifiedTimeString (fileName) :
	gmtime = getModifiedTime(fileName)
	return time.strftime('%a, %d %b %Y %H:%M:%S GMT', gmtime)

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
		if '/' == parts[1][0] :
			parts[1] = path + parts[1]
		else :
			parts[1] = path + '/' + parts[1]
		details['file'] = parts[1]
		details['HTTP'] = parts[2]
		if details['HTTP'] != "HTTP/1.1" :
			raise HTTPVersionNotSupportedException
		if details['type'] != "GET" :
			raise NonGetRequestException

	except IndexError :
		raise BadRequestException

	print(details['type'] + ' ' + details['file'])
	return details

def getContent (details) :
	# process the request
	content = openFile(details['file'])
	return content

def getResponse (details) :
	response  = ""
	response += details["HTTP"] + " " + details["code"] + endl
	response += "Date: " + getCurrentTimeString() + endl
	response += "Server: " + serverName + "/" + serverVersion + " (" + os.name + ")" + endl
	if details["code"] == codeDict[200] :
		response += "Last-Modified: " + details["modified"] + endl
	response += "Accept-Ranges: bytes" + endl
	response += "Content-Length: " + str(len(details["content"])) + endl
	response += "Keep-Alive: timeout=10, max=100" + endl
	response += "Connection: Keep-Alive" + endl
	response += "Content-Type: text/html; charset=ISO-8859-1" + endl
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
		rawRequest = getRequest(clientSocket)

		responseDict = {
			"HTTP" : "HTTP/1.1"
		}

		try :

			# parse the request
			requestDict = parseRequest(rawRequest)

			try :

				responseDict["content"] = getContent(requestDict)
				responseDict["code"] = codeDict[200]
				responseDict["modified"] = getModifiedTimeString(requestDict["file"])

			except NotFoundException :
				print("File not found")
				responseDict["content"] = responseDict["code"] = codeDict[404]

		except NonGetRequestException :
			print("403 Server only accepts GET requests")
			responseDict["content"] = responseDict["code"] = codeDict[403]

		except BadRequestException :
			print("400 Bad request")
			responseDict["content"] = responseDict["code"] = codeDict[400]

		except HTTPVersionNotSupportedException :
			print("505 Server only supports HTTP/1.1")
			responseDict["content"] = responseDict["code"] = codeDict[505]

		rawResponse = getResponse(responseDict)

		returnResponse(rawResponse, clientSocket)

		#close the connection
		clientSocket.close()

print(serverName + "/" + serverVersion)

# define port number and socket
port = getPort()
serverSocket = socket(AF_INET, SOCK_STREAM)

# activate socket
serverSocket.bind(('localhost', port))
serverSocket.listen(1)

listen()
